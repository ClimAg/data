# data

## Climate model datasets

### EURO-CORDEX

<https://euro-cordex.net/>

Generated using the [DKRZ] intake-esm stores

Data specifications:

- Project: CORDEX
- Experiments:
  - historical (1976-2005)
  - rcp45, rcp85 (2041-2070)
- Frequency: day
- Domain: EUR-11 (12.5 km)
- [Variables]: evspsblpot, pr, rsds, tas
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

<https://epa.ie/pubs/reports/research/climate/researchreport339/>

Data specifications:

- Experiments:
  - historical (1976-2005)
  - rcp45, rcp85 (2041-2070)
- Frequency: day
- Resolution: 4 km
- Variables: ET, T_2M, TOT_PREC, ASWDIR_S, ASWDIFD_S
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

## Meteorological data

### Met Éireann Reanalysis (MÉRA)

<https://www.met.ie/climate/available-data/mera>

Variable                  | Identifier     | Unit
--                        | --:            | --
Surface pressure*         | `  1 105  0 0` | Pa
2 m temperature           | ` 11 105  2 0` | K
Maximum temperature*      | ` 15 105  2 2` | K
Minimum temperature*      | ` 16 105  2 2` | K
u-component of 10 m wind* | ` 33 105 10 0` | m s⁻¹
v-component of 10 m wind* | ` 34 105 10 0` | m s⁻¹
2 m relative humidity*    | ` 52 105  2 0` | %
Total precipitation       | ` 61 105  0 4` | kg m⁻²
Net shortwave irradiance* | `111 105  0 4` | J m⁻²
Net longwave irradiance*  | `112 105  0 4` | J m⁻²
Global irradiance         | `117 105  0 4` | J m⁻²

Variables marked with an \* are used to derive evapotranspiration using the FAO Penman-Monteith equation. Note that the irradiance variables are ***incorrectly*** assigned W m⁻² as their unit in the GRIB files.

Variable types (the time-range indicator is the final number in the identifier):

- Instantaneous (time-range indicator equal to 0) parameters produced by the atmospheric model available at or near the surface.
- Accumulated (time-range indicator equal to 4) parameters produced by the atmospheric model available at or near the surface. All accumulations are initiated at the start of each forecast and are valid at the forecast step indicated in the data.
- Parameters that are valid over a specified period of time (time-range indicator equal to 2) produced by the atmospheric model at or near the surface. All such parameters are valid for the previous forecast hour; e.g. the maximum temperature at forecast hour 24 is the maximum temperature between hours 23 and 24. These parameters are reset each hour by the forecast model.

The third timestep of the three-hour forecasts (FC3hr) were taken and resampled to daily resolution. Precipitation and irradiance variables are accumulated over a three-hour period in the third forecast step, so conversions were done during the resampling (see <https://confluence.ecmwf.int/pages/viewpage.action?pageId=197702790>).

© 2019 Met Éireann

Whelan, E., Hanley, J., and Gleeson, E. (2017). The MÉRA Data Archive, Technical Note, Dublin, Ireland, Met Éireann. [Online]. Available at <https://hdl.handle.net/2262/81711> (Accessed 15 November 2022).

### Valentia Observatory time series

Sample data for testing grass growth model. This location was used as it is characterised by a continuous growing season, and was useful in determining the right implementation of the growing season and seasonality in the grass growth model. The data is subset from [raw data][Valentia] downloaded from Met Éireann's servers.

## Site-specific characteristics

### Stocking rate derived using the Census of Agriculture

ROI (CSO)
- <https://www.cso.ie/en/methods/agricultureandfishing/censusofagriculture/censusofagriculture2020/>
- <https://data.cso.ie/table/AVA42>
- <https://data.cso.ie/table/AVA44>

NI (DAERA)
- <https://www.daera-ni.gov.uk/articles/agricultural-census-northern-ireland>
- <https://www.opendatani.gov.uk/@department-of-agriculture-environment-rural-affairs-statistics-analytical-services-branch/farm-census-administrative-geographies>

### Nitrogen nutritional index derived using JRC-ESDAC data

Maps of Soil Chemical properties at European scale based on LUCAS 2009/2012 topsoil data: <https://esdac.jrc.ec.europa.eu/content/chemical-properties-european-scale-based-lucas-topsoil-data>

The chemical properties maps for the European Union were produced using Gaussian process regression (GPR) models. Resolution: 500m. Format: TIFF; projection information: ETRS89 / LAEA Europe. Soil nitrogen distribution is dependent on soil organic carbon, vegetation and climate and soil texture.

With 22,000 sampled locations the LUCAS soil database is unique in Europe for the number of available observations, its spatial coverage and its temporal resolution. The interpolated maps of chemical properties offer a better overview of the distribution of soil chemical properties in the EU to the scientific community and to policy makers. The derived maps will establish baselines that will help monitor soil quality and provide guidance to agro-environmental research and policy developments in the European Union.

### Soil water-holding capacity derived using JRC-ESDAC data

European Soil Database Derived data: <https://esdac.jrc.ec.europa.eu/content/european-soil-database-derived-data>

Total available water content from PTF

## Grass growth measurements

### GrassCheck NI

<https://agrisearch.org/grasscheck>

Grass growth measurements for Northern Ireland

Manually extracted from information provided in GrassCheck weekly bulletins:
<https://www.agrisearch.org/bulletins>

The grass growth data is aggregated at county level and is measured in kg DM ha⁻¹ day⁻¹.
Frequency is weekly.

© 2017-2022 Agrisearch

Huson, K. M., Lively, F. O., Aubry, A., Takahashi, T., Gordon, A., and McDonnell, D. A. (2020).
'GrassCheck: monitoring grass growth and maximizing grass utilisation on UK farms',
in Virkajärvi, P. et al. (eds),
*Meeting the future demands for grassland production*,
Grassland Science in Europe, Helsinki, Finland, European Grassland Federation,
vol. 25, pp. 716–718. [Online][Huson]. (Accessed 13 September 2022).

### PastureBase Ireland

<https://pasturebase.teagasc.ie>

© 2013-2022 Teagasc

Hanrahan, L., Geoghegan, A., O'Donovan, M., Griffith, V., Ruelle, E., Wallace, M., and Shalloo, L. (2017).
'PastureBase Ireland: A grassland decision support system and national database',
*Computers and Electronics in Agriculture*, vol. 136, pp. 193–201.
DOI: [10.1016/j.compag.2017.01.029][Hanrahan].

## Boundaries

### Island of Ireland

NUTS (Nomenclature of territorial units for statistics): <https://ec.europa.eu/eurostat/web/gisco/geodata/reference-data/administrative-units-statistical-units/nuts>

Natural Earth 10 m boundary: <https://www.naturalearthdata.com/downloads/10m-physical-vectors/10m-land/>

## Electoral divisions

The Census of Agriculture data are aggregated by electoral division or ward.

ROI electoral divisions: <https://data-osi.opendata.arcgis.com/datasets/osi::electoral-divisions-osi-national-statutory-boundaries-2019>

UK Wards: <https://geoportal.statistics.gov.uk/datasets/ons::wards-december-2022-boundaries-uk-bfc>

### Counties

The grass growth measurements, PastureBase Ireland and Grass Check NI, are aggregated at county level.

- Ordnance Survey Ireland (OSi) National Statutory Boundaries - 2019:
  <https://data-osi.opendata.arcgis.com/datasets/osi::counties-osi-national-statutory-boundaries-2019/about>

- Ordnance Survey Northern Ireland (OSNI) Open Data - Largescale Boundaries - County Boundaries:
  <https://www.opendatani.gov.uk/dataset/osni-open-data-largescale-boundaries-county-boundaries1>

## Other data (unused in analysis)

### Grass10

Data taken from Teagasc Grass10 newsletters:
<https://www.teagasc.ie/crops/grassland/grass10/>

### Agro-environmental regions in Holden and Brereton (2004)

© 2004 N. M. Holden and A. J. Brereton

Six agroclimatic regions have been derived from the map available in the
following paper:

Holden, N. M. and Brereton, A. J. (2004).
'Definition of agroclimatic regions in Ireland using hydro-thermal and crop yield data',
*Agricultural and Forest Meteorology*, vol. 122, no. 3, pp. 175–191.
DOI: [10.1016/j.agrformet.2003.09.010][Holden].

A screenshot of the map was taken, then georeferenced in [QGIS]/[GDAL] using the steps detailed in `holden_brereton_2004_regions.sh`.

## List of references

Available on Zotero: <https://www.zotero.org/groups/4706660/climag/collections/N6IJMX95>

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
[Nolan]: https://epa.ie/pubs/reports/research/climate/researchreport339/
[QGIS]: https://www.qgis.org/
[Valentia]: https://data.gov.ie/dataset/valentia-observatory-daily-data
[Variables]: https://www.wdc-climate.de/ui/codes?type=IPCC_DDC_AR5
[Wget]: https://www.gnu.org/software/wget/
