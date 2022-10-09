"""eurocordex_ie.py

Subset EURO-CORDEX data for Ireland
"""

# import libraries
import os
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

# subset data for each experiment
for experiment in ["rcp85", "historical"]:
    cordex_eur11 = cordex_eur11_cat.search(
        experiment_id=experiment,
        variable_id=["pr", "tas", "evspsblpot"],
        institute_id="SMHI"
    )

    data = xr.open_mfdataset(
        list(cordex_eur11.df["uri"]),
        chunks="auto",
        decode_coords="all"
    )

    # clip to Ireland's boundary with a 10 km buffer
    data = data.rio.clip(ie.buffer(10000).to_crs(data.rio.crs))

    # convert units
    for v in data.data_vars:
        var_attrs = data[v].attrs  # extract attributes
        if v == "tas":
            var_attrs["units"] = "°C"  # convert K to deg C
            data[v] = data[v] - 273.15
        else:
            var_attrs["units"] = "mm/day"  # convert kg m-2 s-1 to mm/day
            data[v] = data[v] * 60 * 60 * 24
        data[v].attrs = var_attrs  # reassign attributes

    # export to NetCDF
    FILE_NAME = cplt.ie_cordex_ncfile_name(data)

    data.to_netcdf(os.path.join(DATA_DIR, FILE_NAME))
