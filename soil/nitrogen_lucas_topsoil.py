"""nitrogen_lucas_topsoil.py

Nitrogen nutritional index

Soil chemical properties based on LUCAS topsoil data (Ballabio et al., 2019;
European Commission, n.d.; Panagos et al., 2022; Panagos et al., 2012):
https://esdac.jrc.ec.europa.eu/content/chemical-properties-european-scale-based-lucas-topsoil-data
"""

import os
from zipfile import BadZipFile, ZipFile
import geopandas as gpd
import rioxarray as rxr
from rasterstats import zonal_stats

DATA_DIR = os.path.join(
    "data", "soil",
    "chemical-properties-european-scale-based-lucas-topsoil-data"
)

ZIP_FILE = os.path.join(DATA_DIR, "N.zip")

# extract the archive
try:
    z = ZipFile(ZIP_FILE)
    z.extractall(DATA_DIR)
except BadZipFile:
    print("There were issues with the file", ZIP_FILE)

DATA_FILE = os.path.join(DATA_DIR, "N.tif")

data = rxr.open_rasterio(DATA_FILE, chunks="auto", masked=True)

# Ireland boundary
GPKG_BOUNDARY = os.path.join(
    "data", "boundaries", "NUTS2021", "NUTS_2021.gpkg"
)
ie = gpd.read_file(GPKG_BOUNDARY, layer="NUTS_RG_01M_2021_2157_IE")

# clip raster to Ireland's boundary
data = rxr.open_rasterio(
    DATA_FILE, chunks="auto", masked=True
).rio.clip(ie.to_crs(data.rio.crs)["geometry"])

# export to GeoTIFF
data.rio.to_raster(os.path.join(DATA_DIR, "IE_N.tif"))

# ## Grid cells
grid_cells = gpd.read_file(
    os.path.join("data", "ModVege", "params.gpkg"),
    layer="eurocordex"
)

# ## Zonal stats
grid_cells = gpd.GeoDataFrame.from_features(
    zonal_stats(
        vectors=grid_cells.to_crs(data.rio.crs),
        raster=os.path.join(DATA_DIR, "IE_N.tif"),
        stats=["count", "mean"],
        geojson_out=True
    ), crs=data.rio.crs
).to_crs(grid_cells.crs)

# ## Normalise
# normalise between 1.0 and 0.35
grid_cells["ni"] = (
    0.35 + (
        (grid_cells["mean"] - float(grid_cells["mean"].min())) * (1.0 - 0.35)
    ) / (
        float(grid_cells["mean"].max()) - float(grid_cells["mean"].min())
    )
)

# fill no data with min value
grid_cells["ni"] = grid_cells["ni"].fillna(0.35)

grid_cells.drop(columns=["mean", "count"], inplace=True)

grid_cells.to_file(
    os.path.join("data", "ModVege", "params.gpkg"), layer="eurocordex"
)
