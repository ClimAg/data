#!/bin/bash
#
# move the downloaded HiResIreland data into subdirectories

for experiment in historical rcp45 rcp85;
do for gcm in CNRM-CM5 EC-EARTH HadGEM2-ES MPI-ESM-LR MIROC5;
do mkdir -p COSMO5-CLM/${experiment}/${gcm}
mv *${gcm}_${experiment}*.nc COSMO5-CLM/${experiment}/${gcm}
done
done
