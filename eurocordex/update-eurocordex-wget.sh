#!/bin/bash
#
# update ESGF Wget scripts
# remove data files that do not correspond to the study time range
# i.e. outside 1976-2005 and 2041-2070
# replace egrep with grep -E
# add some notes about the modifications

for node in esgf.ceda.ac.uk esg-dn1.nsc.liu.se;
do for filename in $(grep -l $node data/eurocordex/wget-*.sh);
do rm -f -- data/eurocordex/wget-$node.sh &&
awk '
!/19511201/ && !/19560101/ && !/19610101/ && !/19660101/ && !/19700101/ &&
!/19710101/ &&
!/20060101/ && !/20110101/ && !/20160101/ && !/20210101/ && !/20260101/ &&
!/20310101/ && !/20310101/ && !/20360101/ && !/20710101/ && !/20760101/ &&
!/20810101/ && !/20860101/ && !/20910101/ && !/20960101/
' $filename > data/eurocordex/wget-$node.sh &&
sed -i 's/egrep/grep -E/g' data/eurocordex/wget-$node.sh &&
awk -v timestamp="$(date)" '
NR==5{ print "\
# NOTE: this file has been modified to remove data files that do not\
\n# correspond to the study time range, i.e. outside 1976-2005 and 2041-2070.\
\n# Additionally, egrep has been replaced with grep -E.\
\n# Last updated by N. M. Streethran - " timestamp ".\
\n#" }1
' data/eurocordex/wget-$node.sh > temp.sh
mv temp.sh data/eurocordex/wget-$node.sh;
done;
done
