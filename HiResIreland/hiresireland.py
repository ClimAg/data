"""hiresireland.py

Subset HiResIreland data for the Island of Ireland
"""

# import libraries
import glob
import itertools
import os
from datetime import datetime, timezone
import geopandas as gpd
import xarray as xr

DATA_DIR_BASE = os.path.join("data", "HiResIreland")

# Ireland boundary
GPKG_BOUNDARY = os.path.join("data", "boundary", "boundaries.gpkg")
ie = gpd.read_file(GPKG_BOUNDARY, layer="NUTS_Ireland_ITM")

# subset data for each experiment
for experiment in ["rcp85", "historical"]:
    data = xr.open_mfdataset(
        list(itertools.chain(*list(
            glob.glob(os.path.join(DATA_DIR_BASE, experiment, "MPI-ESM-LR", e))
            for e in [
                "*mean_T_2M*.nc", "*ASOB_S*.nc", "*ET*.nc", "*TOT_PREC*.nc"
            ]
        ))),
        chunks="auto",
        decode_coords="all"
    )

    data_crs = data.rio.crs

    # clip to Ireland's boundary
    data = data.rio.clip(ie.buffer(1).to_crs(data_crs))

    # convert units and rename variables
    for v in data.data_vars:
        var_attrs = data[v].attrs  # extract attributes
        if v == "T_2M":
            var_attrs["units"] = "°C"  # convert K to deg C
            data[v] = data[v] - 273.15
            var_attrs["long_name"] = "Near-Surface Air Temperature"
        elif v == "ASOB_S":
            var_attrs["units"] = "MJ m⁻² day⁻¹"
            # convert W m-2 to MJ m-2 day-1
            # Allen (1998) - FAO Irrigation and Drainage Paper No. 56 (p. 45)
            # (per second to per day; then convert to mega)
            data[v] = data[v] * (60 * 60 * 24 / 1e6)
            var_attrs["long_name"] = (
                "Surface Net Downwelling Shortwave Radiation"
            )
        elif v == "TOT_PREC":
            var_attrs["units"] = "mm day⁻¹"  # kg m-2 is the same as mm day-1
            var_attrs["long_name"] = "Precipitation"
        else:
            var_attrs["units"] = "mm day⁻¹"
            var_attrs["long_name"] = "Evapotranspiration"
            var_attrs["standard_name"] = "evapotranspiration"
        data[v].attrs = var_attrs  # reassign attributes

    # rename variables
    data = data.rename({
        "T_2M": "tas", "ASOB_S": "rsds", "TOT_PREC": "pr", "w": "evspsblpot"
    })

    # assign attributes for the data
    data.attrs["comment"] = (
        "This dataset has been clipped with the Island of Ireland's boundary. "
        "Last updated: " + str(datetime.now(tz=timezone.utc)) +
        " by nstreethran@ucc.ie."
    )

    # reassign CRS
    data.rio.write_crs(data_crs, inplace=True)

    # export data
    data.to_netcdf(os.path.join(
        DATA_DIR_BASE,
        experiment,
        "_".join(list(data.data_vars)) + "_" + data.attrs["title"] + ".nc"
    ))
