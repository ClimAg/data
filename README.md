# data

## Climate model outputs

### [EURO-CORDEX](https://euro-cordex.net/)

Generated using the [DKRZ](https://www.dkrz.de/) intake-esm stores

Data specifications:

- Project: CORDEX
- Experiments: historical, rcp85
- Time frequency: day
- Ensemble: r1i1p1
- Domain: EUR-11 (12.5 km)
- [Variables](https://www.wdc-climate.de/ui/codes?type=IPCC_DDC_AR5): evspsblpot, mrso, pr, rsds, tas
- [ESGF](https://esgf.llnl.gov) node: [NSC LIU](https://nsc.liu.se/)
- Driving models:
  - MPI-M-MPI-ESM-LR
  - CNRM-CERFACS-CNRM-CM5
  - IPSL-IPSL-CM5A-MR
  - MOHC-HadGEM2-ES
  - ICHEC-EC-EARTH
  - NCC-NorESM1-M
- RCM: RCA4

To automate downloading these data, run the [Wget](https://www.gnu.org/software/wget/) script(s):

```sh
./wget-esg-dn1.nsc.liu.se.sh
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

### HiResIreland

## Grass growth

### GrassCheck NI

Grass growth measurements for Northern Ireland

Manually extracted from information provided in GrassCheck weekly bulletins: <https://www.agrisearch.org/bulletins>

The grass growth data is aggregated at county level and is measured in kg DM ha⁻¹ day⁻¹. Timestep is weekly.

© 2017-2022 Agrisearch

Huson, K. M., Lively, F. O., Aubry, A., Takahashi, T., Gordon, A. and
McDonnell, D. A. (2020).
'GrassCheck: monitoring grass growth and maximizing grass utilisation on UK
farms', in Virkajärvi, P. et al. (eds),
*Meeting the future demands for grassland production*,
Grassland Science in Europe, Helsinki, Finland, European Grassland Federation,
vol. 25, pp. 716–718. [Online]. Available at
<https://www.europeangrassland.org/fileadmin/documents/Infos/Printed_Matter/Proceedings/EGF2020.pdf>
(Accessed 13 September 2022).

### PastureBase Ireland

© 2013-2022 Teagasc

Hanrahan, L., Geoghegan, A., O'Donovan, M., Griffith, V., Ruelle, E.,
Wallace, M. and Shalloo, L. (2017). 'PastureBase Ireland: A grassland
decision support system and national database',
*Computers and Electronics in Agriculture*, vol. 136, pp. 193–201.
DOI: [10.1016/j.compag.2017.01.029][Hanrahan].

## Climatic regions

### Agro-environmental regions in Holden and Brereton (2004)

© 2004 N. M. Holden and A. J. Brereton

Six agroclimatic regions have been derived from the map available in the following paper:

Holden, N. M. and Brereton, A. J. (2004). 'Definition of agroclimatic regions
in Ireland using hydro-thermal and crop yield data',
*Agricultural and Forest Meteorology*, vol. 122, no. 3, pp. 175–191. DOI:
[10.1016/j.agrformet.2003.09.010][Holden].

A screenshot of the map was taken, then georeferenced in [QGIS](https://www.qgis.org/)/[GDAL](https://gdal.org/) using the steps detailed in `holden_brereton_2004_regions.sh`.

## Licence

Scripts by N. M. Streethran are licensed under the [Apache-2.0 License](https://www.apache.org/licenses/LICENSE-2.0).

[Hanrahan]: https://doi.org/10.1016/j.compag.2017.01.029
[Holden]: https://doi.org/10.1016/j.agrformet.2003.09.010
