# data

## Climate model outputs

### [EURO-CORDEX](https://euro-cordex.net/)

Generated using the [DKRZ](https://www.dkrz.de/) intake-esm stores

Data specifications:

- Project: CORDEX
- Experiments: historical, rcp85
- Time frequency: day
- Ensemble: r1i1p1
- Domain: EUR-11
- [Variables](https://www.wdc-climate.de/ui/codes?type=IPCC_DDC_AR5): evspsblpot, mrso, pr, rlds, rlus, rsds, rsus, sund, tas, tasmax, tasmin

[ESGF](https://esgf.llnl.gov) nodes and models (GCM - global/driving model; RCM - regional climate model):

Node | GCM | RCM | Downscaling realisation
-- | -- | -- | --
[CEDA](https://www.ceda.ac.uk/) | CNRM-CERFACS-CNRM-CM5 | HadREM3-GA7-05 | v2
[NSC LIU](https://nsc.liu.se/) | MPI-M-MPI-ESM-LR | SMHI-RCA4 | v1a

To automate downloading this data, run the [Wget](https://www.gnu.org/software/wget/) script(s):

```sh
./wget-esgf.ceda.ac.uk.sh  # CEDA ESGF node
./wget-esg-dn1.nsc.liu.se.sh  # NSC LIU ESGF node
```

The data will be downloaded to the working directory. To move the files into subdirectories:

```sh
./move-eurocordex-downloads.sh
```

ESGF login credentials will be requested once the script is run. See the [ESGF Wget documentation](https://esgf.github.io/esgf-user-support/faq.html#esgf-wget) for more information. If there is a username/password authentication failure, ensure the ESGF user account being used has joined the CORDEX research group.

Links:

- <https://gitlab.dkrz.de/data-infrastructure-services/intake-esm>
- <https://data-infrastructure-services.gitlab-pages.dkrz.de/tutorials-and-use-cases>
- <https://gitlab.dkrz.de/data-infrastructure-services/intake-esm/>
- <https://intake-esm.readthedocs.io/>
- <https://github.com/intake/intake-esm>
- <https://gallery.pangeo.io/repos/pangeo-data/pangeo-tutorial-gallery/intake.html>
- <https://intake.readthedocs.io/>

## Grass growth

### GrassCheck NI

Grass growth measurements for Northern Ireland

Manually extracted from information provided in GrassCheck weekly bulletins: <https://www.agrisearch.org/bulletins>

The grass growth data is aggregated at county level and is measured in kg DM/ha/day.

© 2022 Agrisearch

## Climatic regions

### Holden and Brereton (2004)

Six agroclimatic regions have been derived from the map available in the following paper:

Holden, N. M. and Brereton, A. J. (2004). 'Definition of agroclimatic regions in Ireland using hydro-thermal and crop yield data', *Agricultural and Forest Meteorology*, vol. 122, no. 3, pp. 175–191. DOI: [10.1016/j.agrformet.2003.09.010](https://doi.org/10.1016/j.agrformet.2003.09.010).

A screenshot of the map was taken (`climatic-regions/holden-brereton-2004/holden_brereton_2004_regions.png`), then georeferenced in [QGIS](https://www.qgis.org/)/[GDAL](https://gdal.org/) using the steps detailed in `climatic-regions/holden-brereton-2004/holden_brereton_2004_regions.sh`.

## Licence

Scripts by N. M. Streethran are licensed under the [Apache-2.0 License](https://www.apache.org/licenses/LICENSE-2.0).
