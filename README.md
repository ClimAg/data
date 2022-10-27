# data

## Boundaries

### Counties

Ordnance Survey Ireland (OSi) National Statutory Boundaries - 2019

<https://data-osi.opendata.arcgis.com/datasets/osi::counties-osi-national-statutory-boundaries-2019/about>

Ordnance Survey Northern Ireland (OSNI) Open Data - Largescale Boundaries - County Boundaries

<https://www.opendatani.gov.uk/dataset/osni-open-data-largescale-boundaries-county-boundaries1>

### Island of Ireland

NUTS (Nomenclature of territorial units for statistics)

<https://ec.europa.eu/eurostat/web/gisco/geodata/reference-data/administrative-units-statistical-units/nuts>

## Climate model outputs

### [EURO-CORDEX](https://euro-cordex.net/)

Generated using the [DKRZ] intake-esm stores

Data specifications:

- Project: CORDEX
- Experiments:
  - historical (1976-2005)
  - rcp45, rcp85 (2041-2070)
- Frequency: day
- Domain: EUR-11 (12.5 km)
- [Variables]: evspsblpot, mrso, pr, rsds, rsus, tas
- [ESGF] node: [NSC LIU](https://nsc.liu.se/)
- Driving models (and ensemble):
  - MPI-M-MPI-ESM-LR (r1i1p1)
  - CNRM-CERFACS-CNRM-CM5 (r1i1p1)
  - MOHC-HadGEM2-ES (r1i1p1)
  - ICHEC-EC-EARTH (r12i1p1)
- RCM: RCA4

To automate downloading these data, run the [Wget] script(s):

```sh
./wget-esg-dn1.nsc.liu.se.sh
```

The data will be downloaded to the working directory.
To move the files into subdirectories:

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

Jacob, D. et al. (2014).
'EURO-CORDEX: new high-resolution climate change projections for European impact research',
Regional Environmental Change, vol. 14, no. 2, pp. 563–578.
DOI: [10.1007/s10113-013-0499-2][Jacob].

### HiResIreland

Data specifications:

- Experiments:
  - historical (1976-2005)
  - rcp45, rcp85 (2041-2070)
- Frequency: day
- [Variables]: evspsblpot, mrso, pr, tas, par
- Driving models (and ensemble):
  - MPI-M-MPI-ESM-LR (r1i1p1)
  - CNRM-CERFACS-CNRM-CM5 (r1i1p1)
  - MOHC-HadGEM2-ES (r1i1p1)
  - ICHEC-EC-EARTH (r12i1p1)
- RCM: COSMO5-CLM

Nolan, P. and Flanagan, J. (2020).
High-resolution Climate Projections for Ireland - A Multi-model Ensemble Approach (2014-CCRP-MS.23),
EPA Research Programme 2014-2020, EPA Research Report,
Johnstown Castle, Co. Wexford, Ireland, Environmental Protection Agency (EPA).
[Online][Nolan]. (Accessed 23 June 2022).

## Grass growth

### GrassCheck NI

Grass growth measurements for Northern Ireland

Manually extracted from information provided in GrassCheck weekly bulletins:
<https://www.agrisearch.org/bulletins>

The grass growth data is aggregated at county level and is measured in kg DM ha⁻¹ day⁻¹.
Frequency is weekly.

© 2017-2022 Agrisearch

Huson, K. M., Lively, F. O., Aubry, A., Takahashi, T., Gordon, A. and McDonnell, D. A. (2020).
'GrassCheck: monitoring grass growth and maximizing grass utilisation on UK farms',
in Virkajärvi, P. et al. (eds),
*Meeting the future demands for grassland production*,
Grassland Science in Europe, Helsinki, Finland, European Grassland Federation,
vol. 25, pp. 716–718. [Online][Huson]. (Accessed 13 September 2022).

### PastureBase Ireland

© 2013-2022 Teagasc

Hanrahan, L., Geoghegan, A., O'Donovan, M., Griffith, V., Ruelle, E., Wallace, M. and Shalloo, L. (2017).
'PastureBase Ireland: A grassland decision support system and national database',
*Computers and Electronics in Agriculture*, vol. 136, pp. 193–201.
DOI: [10.1016/j.compag.2017.01.029][Hanrahan].

### Grass10

Data taken from Teagasc Grass10 newsletters:
<https://www.teagasc.ie/crops/grassland/grass10/>

## Climatic regions

### Agro-environmental regions in Holden and Brereton (2004)

© 2004 N. M. Holden and A. J. Brereton

Six agroclimatic regions have been derived from the map available in the
following paper:

Holden, N. M. and Brereton, A. J. (2004).
'Definition of agroclimatic regions in Ireland using hydro-thermal and crop yield data',
*Agricultural and Forest Meteorology*, vol. 122, no. 3, pp. 175–191.
DOI: [10.1016/j.agrformet.2003.09.010][Holden].

A screenshot of the map was taken, then georeferenced in [QGIS]/[GDAL] using the steps detailed in `holden_brereton_2004_regions.sh`.

## Licence

Scripts by N. M. Streethran are licensed under the [Apache-2.0 License][Apache].

[Apache]: https://www.apache.org/licenses/LICENSE-2.0
[DKRZ]: https://www.dkrz.de/
[ESGF]: https://esgf.llnl.gov
[GDAL]: https://gdal.org/
[Hanrahan]: https://doi.org/10.1016/j.compag.2017.01.029
[Holden]: https://doi.org/10.1016/j.agrformet.2003.09.010
[Huson]: https://www.europeangrassland.org/fileadmin/documents/Infos/Printed_Matter/Proceedings/EGF2020.pdf
[Jacob]: https://doi.org/10.1007/s10113-013-0499-2
[Nolan]: https://www.epa.ie/publications/research/climate-change/research-339-high-resolution-climate-projections-for-ireland--a-multi-model-ensemble-approach.php
[QGIS]: https://www.qgis.org/
[Variables]: https://www.wdc-climate.de/ui/codes?type=IPCC_DDC_AR5
[Wget]: https://www.gnu.org/software/wget/
