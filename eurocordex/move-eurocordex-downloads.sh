#!/bin/bash
#
# move the downloaded EURO-CORDEX data into subdirectories

for experiment in historical rcp85;
do for institute in MOHC SMHI;
do for variable in evspsblpot mrso pr rlds rlus rsds rsus sund tas tasmax tasmin;
do mkdir -p ${institute}/${experiment}/${variable}
mv ${variable}_*_${experiment}_*_${institute}*.nc ${institute}/${experiment}/${variable};
done;
done;
done
