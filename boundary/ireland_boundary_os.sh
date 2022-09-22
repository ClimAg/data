#!/bin/sh

# QGIS commands

# dissolve the county layer
qgis_process run native:dissolve \
--INPUT='data/boundary/boundaries.gpkg|layername=OS_IE_Counties_ITM|geometrytype=Polygon' \
--SEPARATE_DISJOINT=false \
--OUTPUT='ogr:dbname='\''data/boundary/boundaries_temp.gpkg'\'' table="OS_IE_Ireland_ITM_dissolved" (geom)'
# Python command
# params = {
#     'INPUT': 'data/boundary/boundaries.gpkg|layername=OS_IE_Counties_ITM|geometrytype=Polygon',
#     'FIELD': [],
#     'SEPARATE_DISJOINT': False,
#     'OUTPUT': 'ogr:dbname=\'data/boundary/boundaries_temp.gpkg\' table="OS_IE_Ireland_ITM_dissolved" (geom)'
# }
# processing.run("native:dissolve", params)

# remove holes
qgis_process run native:deleteholes \
--INPUT='data/boundary/boundaries-temp.gpkg|layername=OS_IE_Ireland_ITM_dissolved|geometrytype=Polygon' \
--MIN_AREA=0 \
--OUTPUT='ogr:dbname='\''data/boundary/boundaries.gpkg'\'' table="OS_IE_Ireland_ITM" (geom)'
# Python command
# params = {
#     'INPUT': 'data/boundary/boundaries-temp.gpkg|layername=OS_IE_Ireland_ITM_dissolved|geometrytype=Polygon',
#     'MIN_AREA': 0,
#     'OUTPUT': 'ogr:dbname=\'data/boundary/boundaries.gpkg\' table="OS_IE_Ireland_ITM" (geom)'
# }
# processing.run("native:deleteholes", params)

# reproject to EPSG:4326
qgis_process run native:reprojectlayer \
--INPUT='data/boundary/boundaries.gpkg|layername=OS_IE_Ireland_ITM' \
--TARGET_CRS='EPSG:4326' \
--OPERATION='+proj=pipeline +step +inv +proj=tmerc +lat_0=53.5 +lon_0=-8 +k=0.99982 +x_0=600000 +y_0=750000 +ellps=GRS80 +step +proj=unitconvert +xy_in=rad +xy_out=deg' \
--OUTPUT='ogr:dbname='\''data/boundary/boundaries.gpkg'\'' table="OS_IE_Ireland" (geom)'
# Python command
# params = {
#     'INPUT': 'data/boundary/boundaries.gpkg|layername=OS_IE_Ireland_ITM',
#     'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:4326'),
#     'OPERATION': '+proj=pipeline +step +inv +proj=tmerc +lat_0=53.5 +lon_0=-8 +k=0.99982 +x_0=600000 +y_0=750000 +ellps=GRS80 +step +proj=unitconvert +xy_in=rad +xy_out=deg',
#     'OUTPUT': 'ogr:dbname=\'data/boundary/boundaries.gpkg\' table="OS_IE_Ireland" (geom)'
# }
# processing.run("native:reprojectlayer", params)
