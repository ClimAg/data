"""agricultural_census_gridded.py

Gridding agricultural census data

Gridding based on
<https://james-brennan.github.io/posts/fast_gridding_geopandas/>
"""

# import libraries
import os
import itertools
import geopandas as gpd
import numpy as np
import shapely
import xarray as xr

# ## Open some gridded climate data
TS_FILE_EC = os.path.join(
    "data", "EURO-CORDEX", "IE",
    "IE_EUR-11_ICHEC-EC-EARTH_rcp85_r12i1p1_SMHI-RCA4_v1_day_"
    "20410101-20701231.nc"
)

TS_FILE_HRI = os.path.join(
    "data", "HiResIreland", "IE", "IE_COSMO5_MPI-ESM-LR_rcp45_4km.nc"
)

for dat in [TS_FILE_EC, TS_FILE_HRI]:
    data = xr.open_dataset(dat, chunks="auto", decode_coords="all")

    # keep only one variable
    data = data.drop_vars(names=["PET", "PP", "RG", "PAR"])

    # copy CRS
    crs = data.rio.crs

    # ## Use the gridded data's bounds to generate a gridded vector layer
    xmin, ymin, xmax, ymax = data.rio.bounds()
    # the difference between two adjacent rotated lat or lon values is the
    # cell size
    cell_size = float(data["rlat"][1] - data["rlat"][0])

    # create the cells in a loop
    grid_cells = []
    for x0 in np.arange(xmin, xmax + cell_size, cell_size):
        for y0 in np.arange(ymin, ymax + cell_size, cell_size):
            # bounds
            x1 = x0 - cell_size
            y1 = y0 + cell_size
            grid_cells.append(shapely.geometry.box(x0, y0, x1, y1))
    grid_cells = gpd.GeoDataFrame(grid_cells, columns=["geometry"], crs=crs)

    # ## Drop grid cells without climate data
    grid_centroids = {
        "wkt": [],
        "rlon": [],
        "rlat": []
    }

    for rlon, rlat in itertools.product(
        range(len(data.coords["rlon"])),
        range(len(data.coords["rlat"]))
    ):
        data__ = data.isel(rlon=rlon, rlat=rlat)

        # ignore null cells
        if not data__["T"].isnull().all():
            grid_centroids["wkt"].append(
                f"POINT ({float(data__['rlon'].values)} "
                f"{float(data__['rlat'].values)})"
            )
            grid_centroids["rlon"].append(float(data__["rlon"].values))
            grid_centroids["rlat"].append(float(data__["rlat"].values))

    grid_centroids = gpd.GeoDataFrame(
        grid_centroids,
        geometry=gpd.GeoSeries.from_wkt(grid_centroids["wkt"], crs=crs)
    )

    grid_cells = gpd.sjoin(grid_cells, grid_centroids.to_crs(grid_cells.crs))

    grid_cells.drop(columns=["wkt", "index_right"], inplace=True)

    # ## Read stocking rate data
    stocking_rate = gpd.read_file(
        os.path.join(
            "data", "agricultural_census", "agricultural_census.gpkg"
        ),
        layer="stocking_rate"
    )

    # ## Reproject cells to the CRS of the stocking rate data
    # use a projected CRS (e.g. 2157) instead of a geographical CRS (e.g. 4326)
    grid_cells = grid_cells.to_crs(stocking_rate.crs)

    # ## Create gridded stocking rate data
    merged = gpd.sjoin(stocking_rate, grid_cells, how="left")

    # compute stats per grid cell, use the mean stocking rate
    dissolve = merged[["stocking_rate", "index_right", "geometry"]].dissolve(
        by="index_right", aggfunc=np.mean
    )

    # merge with cell data
    grid_cells.loc[dissolve.index, "stocking_rate"] = (
        dissolve["stocking_rate"].values
    )

    # drop rows with missing values
    grid_cells.dropna(inplace=True)

    # export as GPKG layer
    if data.attrs["contact"] == "rossby.cordex@smhi.se":
        grid_cells.to_file(
            os.path.join("data", "ModVege", "params_eurocordex.gpkg"),
            layer="stocking_rate"
        )
    else:
        grid_cells.to_file(
            os.path.join("data", "ModVege", "params_hiresireland.gpkg"),
            layer="stocking_rate"
        )
