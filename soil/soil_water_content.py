"""soil_water_content.py

Soil water-holding capacity

European soil database derived data - total available water content (TAWC)
for the topsoil [mm] (European Commission, n.d.; Hiederer, 2013a;
Hiederer, 2013b):
https://esdac.jrc.ec.europa.eu/content/european-soil-database-derived-data
"""

import os
from zipfile import BadZipFile, ZipFile

import geopandas as gpd
import rioxarray as rxr
from rasterstats import zonal_stats

DATA_DIR = os.path.join("data", "soil", "european-soil-database-derived-data")

ZIP_FILE = os.path.join(DATA_DIR, "STU_EU_Layers.zip")

# extract the archive
try:
    z = ZipFile(ZIP_FILE)
    z.extractall(DATA_DIR)
except BadZipFile:
    print("There were issues with the file", ZIP_FILE)

DATA_FILE = os.path.join(DATA_DIR, "STU_EU_T_TAWC.rst")

data = rxr.open_rasterio(DATA_FILE, chunks="auto", masked=True)

# assign the right CRS - ETRS 89 LAEA
data_crs = 3035

data.rio.write_crs(data_crs, inplace=True)

# Ireland boundary
GPKG_BOUNDARY = os.path.join("data", "boundaries", "boundaries_all.gpkg")
ie = gpd.read_file(GPKG_BOUNDARY, layer="NUTS_RG_01M_2021_2157_IE")

# clip raster to Ireland's boundary
data = rxr.open_rasterio(DATA_FILE, chunks="auto", masked=True).rio.clip(
    ie.to_crs(data_crs)["geometry"]
)

# export to GeoTIFF
data.rio.to_raster(os.path.join(DATA_DIR, "IE_TAWC.tif"))

# ## Grid cells
grid_cells = gpd.read_file(
    os.path.join("data", "ModVege", "params.gpkg"), layer="eurocordex"
)

# ## Zonal stats
grid_cells = gpd.GeoDataFrame.from_features(
    zonal_stats(
        vectors=grid_cells.to_crs(data_crs),
        raster=os.path.join(DATA_DIR, "IE_TAWC.tif"),
        stats=["count", "mean"],
        geojson_out=True,
        nodata=-999999,
    ),
    crs=data_crs,
).to_crs(grid_cells.crs)

grid_cells["whc"] = grid_cells["mean"]

grid_cells.drop(columns=["mean", "count"], inplace=True)

grid_cells.to_file(
    os.path.join("data", "ModVege", "params.gpkg"), layer="eurocordex"
)
