#!/bin/bash
#
# update ESGF Wget scripts
# - remove data files that do not correspond to the study time range
#   i.e. outside 1976-2005 and 2041-2070
# - an additional year is included (1975 and 2040) to spin-up the model
# - replace egrep with grep -E
# - add some notes about the modifications
# this script assumes that the original Wget scripts downloaded from the
# ESGF portal are in the working directory

for node in esg-dn1.nsc.liu.se;
do rm -f -- wget-${node}.sh
for filename in $(grep -l ${node} wget-*.sh);
do awk '
!/19700101/ &&
!/20060101/ && !/20110101/ && !/20160101/ && !/20210101/ && !/20260101/ &&
!/20310101/ &&
!/20710101/ && !/20760101/ && !/20810101/ && !/20860101/ && !/20910101/ &&
!/20960101/
' ${filename} > wget-${node}.sh
sed -i 's/egrep/grep -E/g' wget-${node}.sh
sed -i 's/[ \t]*$//' wget-${node}.sh
awk -v timestamp="$(date)" '
NR==5{ print "\
# NOTE: this file has been modified to remove data files that do not\
\n# correspond to the study time range, i.e. outside 1976-2005 and 2041-2070.\
\n# Additionally, egrep has been replaced with grep -E.\
\n# Last updated by N. M. Streethran - " timestamp ".\
\n#" }1
' wget-${node}.sh > temp.sh
mv temp.sh wget-${node}.sh
done
done
