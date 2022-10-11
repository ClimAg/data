"""eurocordex_ie.py

Subset EURO-CORDEX data for the Island of Ireland
"""

# import libraries
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

# subset data for each experiment
for experiment in ["rcp85", "historical"]:
    cordex_eur11 = cordex_eur11_cat.search(
        experiment_id=experiment,
        variable_id=["pr", "tas", "evspsblpot", "rsds", "rsus"],
        institute_id="SMHI"
    )

    data = xr.open_mfdataset(
        list(cordex_eur11.df["uri"]),
        chunks="auto",
        decode_coords="all"
    )

    # clip to Ireland's boundary with a 10 km buffer
    data = data.rio.clip(ie.buffer(10000).to_crs(data.rio.crs))

    for v in data.data_vars:
        var_attrs = data[v].attrs  # extract attributes
        if v == "tas":
            var_attrs["units"] = "°C"  # convert K to deg C
            data[v] = data[v] - 273.15
        elif v in ("rsds", "rsus"):
            # convert W m-2 to MJ m-2 day-1
            # from Allen (1998) - FAO Irrigation and Drainage Paper No. 56
            # (p. 45)
            var_attrs["units"] = "MJ m⁻² day⁻¹"
            data[v] = data[v] * 0.0864
        else:
            var_attrs["units"] = "mm day⁻¹"  # convert kg m-2 s-1 to mm day-1
            data[v] = data[v] * 60 * 60 * 24  # (per second to per day)
        data[v].attrs = var_attrs  # reassign attributes

    # assign attributes for the data
    data.attrs["comment"] = (
        "This data has been clipped with the Island of Ireland's boundary. "
        "Last updated: " + str(datetime.now(tz=timezone.utc)) +
        " by nstreethran@ucc.ie."
    )

    # export to NetCDF
    FILE_NAME = cplt.ie_cordex_ncfile_name(data)

    data.to_netcdf(os.path.join(DATA_DIR, FILE_NAME))
