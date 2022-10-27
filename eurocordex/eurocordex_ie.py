"""eurocordex_ie.py

Subset EURO-CORDEX data for the Island of Ireland
"""

# import libraries
import itertools
import os
from datetime import datetime, timezone
import geopandas as gpd
import intake
import xarray as xr
import climag.plot_configs as cplt

DATA_DIR_BASE = os.path.join("data", "eurocordex")

# directory to store outputs
DATA_DIR = os.path.join(DATA_DIR_BASE, "IE")
os.makedirs(DATA_DIR, exist_ok=True)

# Ireland boundary
GPKG_BOUNDARY = os.path.join("data", "boundary", "boundaries.gpkg")
ie = gpd.read_file(GPKG_BOUNDARY, layer="NUTS_Ireland_ITM")

# reading the local catalogue
JSON_FILE_PATH = os.path.join(
    DATA_DIR_BASE, "eurocordex_eur11_local_disk.json"
)

cordex_eur11_cat = intake.open_esm_datastore(JSON_FILE_PATH)

# subset data for each experiment and driving model
driving_model_id = list(cordex_eur11_cat.df["driving_model_id"].unique())

experiment_id = list(cordex_eur11_cat.df["experiment_id"].unique())

for exp, model in itertools.product(experiment_id, driving_model_id):
    cordex_eur11 = cordex_eur11_cat.search(
        experiment_id=exp,
        driving_model_id=model
    )

    data = xr.open_mfdataset(
        list(cordex_eur11.df["uri"]),
        chunks="auto",
        decode_coords="all"
    )

    # copy time_bnds coordinates
    data_time_bnds = data.coords["time_bnds"]

    # copy CRS
    data_crs = data.rio.crs

    # clip to Ireland's boundary
    data = data.rio.clip(ie.buffer(500).to_crs(data.rio.crs))

    # reassign time_bnds
    data.coords["time_bnds"] = data_time_bnds

    # calculate photosynthetically active radiation (PAR)
    # Papaioannou et al. (1993) - irradiance ratio
    data = data.assign(par=(data["rsds"] + data["rsus"]) * 0.473)

    # drop original radiation data
    data = data.drop_vars(["rsds", "rsus"])

    # convert variable units and assign attributes
    for v in data.data_vars:
        var_attrs = data[v].attrs  # extract attributes
        if v == "tas":
            var_attrs["units"] = "°C"  # convert K to deg C
            data[v] = data[v] - 273.15
        elif v == "par":
            # convert W m-2 to MJ m-2 day-1
            # Allen (1998) - FAO Irrigation and Drainage Paper No. 56 (p. 45)
            # (per second to per day; then convert to mega)
            var_attrs["units"] = "MJ m⁻² day⁻¹"
            data[v] = data[v] * (60 * 60 * 24 / 1e6)
            var_attrs["long_name"] = (
                "Surface Photosynthetically Active Radiation"
            )
        elif v == "mrso":
            var_attrs["units"] = "mm day⁻¹"  # kg m-2 is the same as mm day-1
        elif v in ("pr", "evspsblpot"):
            var_attrs["units"] = "mm day⁻¹"  # convert kg m-2 s-1 to mm day-1
            data[v] = data[v] * 60 * 60 * 24  # (per second to per day)
        data[v].attrs = var_attrs  # reassign attributes

    # assign attributes for the data
    data.attrs["comment"] = (
        "This dataset has been clipped with the Island of Ireland's boundary."
        " Last updated: " + str(datetime.now(tz=timezone.utc)) +
        " by nstreethran@ucc.ie."
    )

    data.rio.write_crs(data_crs, inplace=True)

    # export to NetCDF
    FILE_NAME = cplt.ie_cordex_ncfile_name(data)

    data.to_netcdf(os.path.join(DATA_DIR, FILE_NAME))
