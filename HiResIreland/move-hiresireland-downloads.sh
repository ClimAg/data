#!/bin/bash
#
# move the downloaded HiResIreland data into subdirectories

for rcm in COSMO5;
do for experiment in historical rcp45 rcp85;
do for gcm in CNRM-CM5 EC-EARTH HadGEM2-ES MPI-ESM-LR MIROC5;
do mkdir -p ${rcm}/${experiment}/${gcm}
mv *_${rcm}_${gcm}_${experiment}*.nc ${rcm}/${experiment}/${gcm};
done;
done;
done
