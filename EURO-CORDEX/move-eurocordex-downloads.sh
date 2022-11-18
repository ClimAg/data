#!/bin/bash
#
# move the downloaded EURO-CORDEX data into subdirectories

for experiment in historical rcp45 rcp85;
do for gcm in CNRM-CM5 EC-EARTH HadGEM2-ES MPI-ESM-LR;
do mkdir -p RCA4/${experiment}/${gcm}
mv *${gcm}_${experiment}*.nc RCA4/${experiment}/${gcm};
done;
done
