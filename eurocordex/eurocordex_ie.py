# Subset EURO-CORDEX data for Ireland

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

# Cork Airport met station coords
LON = -8.48611
LAT = 51.84722

# Ireland boundary
GPKG_BOUNDARY = os.path.join("data", "boundary", "boundaries.gpkg")
ie = gpd.read_file(GPKG_BOUNDARY, layer="OS_IE_Ireland_ITM")

# reading the local catalogue
JSON_FILE_PATH = os.path.join(
    DATA_DIR_BASE, "eurocordex_eur11_local_disk.json"
)

cordex_eur11_cat = intake.open_esm_datastore(JSON_FILE_PATH)

# precipitation

# filter data subset
cordex_eur11 = cordex_eur11_cat.search(
    experiment_id="rcp85",
    variable_id="pr",
    institute_id="SMHI"
)

data = xr.open_mfdataset(
    list(cordex_eur11.df["uri"]),
    chunks="auto",
    decode_coords="all"
)

# clip to Ireland's bounding box with a 10 km buffer
data = data.rio.clip(ie.envelope.buffer(10000).to_crs(data.rio.crs))

# export to NetCDF
FILE_NAME = cplt.ie_ncfile_name(data)

data.to_netcdf(os.path.join(DATA_DIR, FILE_NAME))

# evapotranspiration

# filter data subset
cordex_eur11 = cordex_eur11_cat.search(
    experiment_id="rcp85",
    variable_id="evspsblpot",
    institute_id="SMHI"
)

data = xr.open_mfdataset(
    list(cordex_eur11.df["uri"]),
    chunks="auto",
    decode_coords="all"
)

# clip to Ireland's bounding box with a 10 km buffer
data = data.rio.clip(ie.envelope.buffer(10000).to_crs(data.rio.crs))

# export to NetCDF
FILE_NAME = cplt.ie_ncfile_name(data)

data.to_netcdf(os.path.join(DATA_DIR, FILE_NAME))

# temperature

# filter data subset
cordex_eur11 = cordex_eur11_cat.search(
    experiment_id="rcp85",
    variable_id="tas",
    institute_id="SMHI"
)

data = xr.open_mfdataset(
    list(cordex_eur11.df["uri"]),
    chunks="auto",
    decode_coords="all"
)

# clip to Ireland's bounding box with a 10 km buffer
data = data.rio.clip(ie.envelope.buffer(10000).to_crs(data.rio.crs))

# export to NetCDF
FILE_NAME = cplt.ie_ncfile_name(data)

data.to_netcdf(os.path.join(DATA_DIR, FILE_NAME))
