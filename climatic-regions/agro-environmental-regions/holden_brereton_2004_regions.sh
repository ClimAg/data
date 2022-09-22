#!/bin/sh

# GDAL/QGIS commands

# georeference screenshot of the 7-cluster agroclimatic regions map from
# Holden and Brereton (2004)
# Holden, N. M. and Brereton, A. J. (2004). ‘Definition of agroclimatic
# regions in Ireland using hydro-thermal and crop yield data’, Agricultural
# and Forest Meteorology, vol. 122, no. 3, pp. 175–191.
# DOI: 10.1016/j.agrformet.2003.09.010.

# georeference the screenshot (holden_brereton_2004_regions.png) using seven
# ground control points
gdal_translate -of GTiff \
    -gcp 484.656 117.3 665879 939165 \
    -gcp 489.711 782.459 673316 597501 \
    -gcp 146.949 827.329 490923 570073 \
    -gcp 211.252 335.908 525775 824434 \
    -gcp 230.659 558.076 537836 710807 \
    -gcp 611.761 597.123 734325 692496 \
    -gcp 593.322 370.719 724129 807354 \
    "data/climatic-regions/agro-environmental-regions/holden_brereton_2004_regions.png" \
    "data/climatic-regions/agro-environmental-regions/holden_brereton_2004_regions_temp.png"

# warp (reproject) the georeferenced raster into ITM (EPSG:2157)
# gdalwarp -t_srs EPSG:2157 -r cubic -of GTiff \
gdalwarp -t_srs EPSG:2157 -r cubic -order 1 -of GTiff -co COMPRESS=NONE -co BIGTIFF=IF_NEEDED \
    "data/climatic-regions/agro-environmental-regions/holden_brereton_2004_regions_temp.png" \
    "data/climatic-regions/agro-environmental-regions/holden_brereton_2004_regions.tif"

# use the projected raster to manually draw features (polygons) of the six
# regions and save it as a vector layer (regions-polygons.gpkg)

# clip the regions using the OS boundary layer for the Island of Ireland
qgis_process run native:clip \
--INPUT='data/climatic-regions/agro-environmental-regions/regions-polygons.gpkg|layername=regions-polygons' \
--OVERLAY='data/boundary/boundaries.gpkg|layername=OS_IE_Ireland_ITM' \
--OUTPUT='ogr:dbname='\''data/climatic-regions/agro-environmental-regions/agro-environmental-regions.gpkg'\'' table="agro-environmental-regions_ITM" (geom)'
# Python command
# params = {
#     'INPUT': 'data/climatic-regions/agro-environmental-regions/regions-polygons.gpkg|layername=regions-polygons',
#     'OVERLAY': 'data/boundary/boundaries.gpkg|layername=OS_IE_Ireland_ITM',
#     'OUTPUT': 'ogr:dbname=\'data/climatic-regions/agro-environmental-regions/agro-environmental-regions.gpkg\' table="agro-environmental-regions_ITM" (geom)'
# }
# processing.run("native:clip", params)

# reproject the layer to EPSG:4326
qgis_process run native:reprojectlayer \
--INPUT='data/climatic-regions/agro-environmental-regions/agro-environmental-regions.gpkg|layername=agro_climatic_regions' \
--TARGET_CRS='EPSG:4326' \
--OPERATION='+proj=pipeline +step +inv +proj=tmerc +lat_0=53.5 +lon_0=-8 +k=0.99982 +x_0=600000 +y_0=750000 +ellps=GRS80 +step +proj=unitconvert +xy_in=rad +xy_out=deg' \
--OUTPUT='ogr:dbname='\''data/climatic-regions/agro-environmental-regions/agro-environmental-regions.gpkg'\'' table="agro-environmental-regions" (geom)'
# Python command
# params = {
#     'INPUT': 'data/climatic-regions/agro-environmental-regions/agro-environmental-regions.gpkg|layername=agro_climatic_regions',
#     'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:4326'),
#     'OPERATION': '+proj=pipeline +step +inv +proj=tmerc +lat_0=53.5 +lon_0=-8 +k=0.99982 +x_0=600000 +y_0=750000 +ellps=GRS80 +step +proj=unitconvert +xy_in=rad +xy_out=deg',
#     'OUTPUT': 'ogr:dbname=\'data/climatic-regions/agro-environmental-regions/agro-environmental-regions.gpkg\' table="agro-environmental-regions" (geom)'
# }
# processing.run("native:reprojectlayer", params)
