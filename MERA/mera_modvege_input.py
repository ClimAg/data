"""mera_modvege_input.py

Met Éireann Reanalysis - generate ModVege input data
"""

# import libraries
import glob
import os
import sys
from datetime import datetime, timezone
import pandas as pd
import xarray as xr
from data.MERA.mera_data_et import mera_calculate_et


def mera_modvege_input(years, spinup=False):

    print("Compiling ModVege input data...", datetime.now(tz=timezone.utc))

    mera_calculate_et(years)

    # directory of processed MÉRA netCDF files
    DATA_DIR = os.path.join("/run/media/nms/MyPassport", "MERA", "netcdf_day")

    # list of netCDF variable files
    var_list = [
        "11_105_2_0",  # 2 m temperature
        "61_105_0_4",  # total precipitation
        "117_105_0_4",  # global irradiance
        "PET",  # evapotranspiration
    ]

    # dictionary to store Xarray datasets
    ds = {}

    for var in var_list:
        ds[var] = xr.open_mfdataset(
            glob.glob(os.path.join(
                DATA_DIR, f"MERA_{years[0]}_{years[1]}_{var}_day.nc"
            )),
            chunks="auto",
            decode_coords="all",
        )

    # obtain CRS info
    data_crs = ds["11_105_2_0"].rio.crs

    # drop the height dimension from the datasets
    for v in var_list[:-1]:
        ds[v] = ds[v].isel(height=0)

    # ## Calculate photosynthetically active radiation (PAR)

    # Papaioannou et al. (1993) - irradiance ratio
    ds["117_105_0_4"] = ds["117_105_0_4"].assign(
        PAR=ds["117_105_0_4"]["grad"] * 0.473
    )
    ds["117_105_0_4"]["PAR"].attrs[
        "long_name"
    ] = "Surface Photosynthetically Active Radiation"
    ds["117_105_0_4"]["PAR"].attrs["units"] = "MJ m⁻² day⁻¹"

    # ## Merge datasets

    # merge datasets
    ds = xr.combine_by_coords(
        [ds["11_105_2_0"], ds["61_105_0_4"], ds["117_105_0_4"], ds["PET"]],
        combine_attrs="drop_conflicts",
        compat="override",
    )

    # drop global radiation
    ds = ds.drop_vars(["grad"])

    # rename other variables
    ds = ds.rename({"t": "T", "tp": "PP"})

    # assign dataset name
    ds.attrs["dataset"] = "IE_MERA_FC3hr_3_day"

    # reassign CRS
    ds.rio.write_crs(data_crs, inplace=True)

    if spinup:
        # ## Extend data to spin-up year

        # copy first year data
        ds_interp = ds.interp(
            time=pd.date_range(
                f"{years[0] - 1}-01-01", f"{years[0] - 1}-12-31", freq="D"
            ),
            kwargs={"fill_value": None},
        )

        ds_interp.rio.write_crs(data_crs, inplace=True)

        # merge spin-up year with first two years of the main data
        ds_interp = xr.combine_by_coords(
            [ds_interp, ds.sel(time=slice(str(years[0]), str(years[0] + 1)))]
        )

        # shift first year of the main data to the spin-up year
        ds_interp = ds_interp.shift(
            time=-ds_interp.sel(time=str(years[0])).dims["time"]
        )

        # keep only spin-up year
        ds_interp = ds_interp.sel(time=str(years[0]))

        # merge with main dataset
        ds = xr.combine_by_coords([ds, ds_interp])

    ds.rio.write_crs(data_crs, inplace=True)

    # ## Save data

    ds.to_netcdf(os.path.join(
        "data", "MERA", f"{ds.attrs['dataset']}_{years[0]}_{years[1]}.nc"
    ))

    print("Done!", datetime.now(tz=timezone.utc))

    sys.exit()


mera_modvege_input(years=(2012, 2019))
