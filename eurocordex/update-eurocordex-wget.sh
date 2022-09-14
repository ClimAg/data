#!/bin/bash

# remove data files that do not correspond to the study time range
# i.e. outside 1976-2005 and 2041-2070

awk '
    !/19700101/ && !/19710101/ && !/20060101/ && !/20110101/ && !/20160101/ &&
    !/20210101/ && !/20260101/ && !/20310101/ && !/20310101/ && !/20360101/ &&
    !/20710101/ && !/20760101/ && !/20810101/ && !/20860101/ && !/20910101/ &&
    !/20960101/
' data/eurocordex/wget-*-ceda.sh > data/eurocordex/eurocordex-wget-ceda.sh

awk '
NR==5{ print "\
# NOTE: this file has been modified to remove data files\
\n# that do not correspond to the study time range,\
\n# i.e. outside 1976-2005 and 2041-2070\
\n#" }1
' data/eurocordex/eurocordex-wget-ceda.sh > temp.sh
mv temp.sh data/eurocordex/eurocordex-wget-ceda.sh

###########################################################################

awk '
    !/19700101/ && !/19710101/ && !/20060101/ && !/20110101/ && !/20160101/ &&
    !/20210101/ && !/20260101/ && !/20310101/ && !/20310101/ && !/20360101/ &&
    !/20710101/ && !/20760101/ && !/20810101/ && !/20860101/ && !/20910101/ &&
    !/20960101/
' data/eurocordex/wget-*-liu.sh > data/eurocordex/eurocordex-wget-liu.sh

awk '
NR==5{ print "\
# NOTE: this file has been modified to remove data files\
\n# that do not correspond to the study time range,\
\n# i.e. outside 1976-2005 and 2041-2070\
\n#" }1
' data/eurocordex/eurocordex-wget-liu.sh > temp.sh
mv temp.sh data/eurocordex/eurocordex-wget-liu.sh
