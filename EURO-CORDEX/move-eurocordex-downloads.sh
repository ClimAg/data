#!/bin/bash
#
# move the downloaded EURO-CORDEX data into subdirectories

for rcm in RCA4;
do for experiment in historical rcp45 rcp85;
do for gcm in CNRM-CM5 EC-EARTH HadGEM2-ES MPI-ESM-LR;
do mkdir -p ${rcm}/${experiment}/${gcm}
mv *${gcm}_${experiment}_*${rcm}*.nc ${rcm}/${experiment}/${gcm};
done;
done;
done
