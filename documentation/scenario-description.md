
# ANGUS II Scenario description


## Overview

The developed scenarios are based on the TYNDP2018, the NEP2019, the Ehighway 100%RES
scenario and the UBA RESCUE scenarios.

For the non-german countries the following data has been used:

* 2030: TYNDP2018 DG (distributed generation vision)
* 2040: TYNDP2018 2040 GCA (global climate action vision)
* 2050: E-Highway 100% RES

For Germany the starting point for the pathyways is the NEP2019:

 * 2030: NEP 2019 C
 * 2040: Interpolated (TYNDP2018)
 * 2050: RESCUE, E-Highway

The scenarios from literature and their different visions have been selected
to model a pathway towards 100% renewable energy system in Germany to
adhere to the COP paris agreement.

## Assumptions

### Spatial and temporal resolution

**Assumptions**: The scenarios model the western europe energy system with one
node per country, i.e. reflecting the market zones. Countries modelled are:
**AT, BE, CH, CZ, DE, DK, FR, IT, NL, NO, PL, SE.**
 The model simulates the the system on an hourly basis for one year using a
 perfect foresight approach with the years 2030, 2040 and 2050.

**Implications & Limitations**: Intra-country grid constraints are not
reflected by the model. Hence, renewable energy  curtailment and/or storage
demand may be underestimated.

## Demand

## Conventional electricity demand
The german efficiency goals to reduce the electricity by 10% until 2020 and 25%
by 2050 % compared to 2008 levels (538.4 TWh) are ambitious but necessary.
Development strongly depends on demographic and economic development
as well as implemented efficiency measures.  While in the basis scenario of the
german Langfristszenarien 441.2 TWh (2030) and 417.2 TWh (2050) are consumed by
conventional electricity applications, the demand in the NEP2019 scenarios for
2030 is higher 477 TWh.

For the ANGUS scenarios the NEP2019 Demand of 477 TWh for 2030 decreases
until 2050 to 403.8 TWh (-25 % compared to 2008).

## Sector coupling
Despite a decreasing demand due to efficiency measure,  the electrification of other
sectors (heat, transport) will create additional demand for electricity.
Currently the heat demand for residential heating accounts for 122.4 TWh hotwater
and 678.5 TWh space heating (2017). The german goals 60 to 80% reduction in heat
demand. With 436.8 TWh (GL) and 246.2 (GS) in the RESCUE scenarios
the reduction is approx. 50 % and 72 % resp. compared to 2008 (889 TWh).

The supply fot this heat demand is based on electricity (heatpumps) to 74.6 % (GS)
and 65 % (GL). The remaining energy is provided by district heating 62.4 TWh (GS)
and in the case of the GL also additional decentral gas boilers.

NEP2019 2030C 29 TWh for heatpumps in residential heating and 25 TWh additional demand
for electric vehicles. In the BMWI 17.8 TWh electricity for heatpumps is assumend.
These values are in the range with the RESCUE green late (GL) and green supreme (GS)
scenarios with 57 TWh_th and 95 TWh_th respectively (assuming coeffienct of
performance of appr. 3). Therefore, for 2040 and 2050 these both RESCUE scenarios
are used as a basis for additional electric heat. For consistency, the electric
demand is also based on these two RESCUE scenarios.

Demand profiles are calculated from the OPSD dataset of the ENTSOE
timeseries for the selected weather year (2012).

*Implications & Limitations*:

* Due to the historic demand profiles, future
flexibilities like smart operation of certain applications and inducstry
processes are not modelled.
* The model only covers the residential hotwater and space heating demand.


## Generation capacity

For Germany installed capacities of the NEPScenario 2019 2030C are implemented.

![Installed capacities](installed_capacities.pdf)


### Conventional energies

Efficiencies are based on the TYNDP2018. However, For germany the OPSD powerplant
register is used to calculate efficiencies for the conventional powerplants in 2030.
Commodity costs are based on the NEP2030C and TYNDP2018 cost assumptions
The availability factor (avf) of technologies and variable
operation and maintenance cost (vom) are the same for all scenarios.

### Renewable Energies
* Maximum biomass potential per country the hotmaps potential is used. The
installed capacity of biomass is assumed to be `biofuels` and `others-res`
from the TNYDP2018.
* For the renewable profiles of wind and pv timeseries of renewables ninja has
been used.
* Hydro reservoir and run of river capacities are assumend to be the same as in 2015. The
inflow in run of river and reservoirs is modelled based on the inflow timeseries
of the Restore2050 project.

## Annex

### Installed capacities Germany

| name          |   ANGUS2030 |   ANGUS2040 |   ANGUS2050 |
|:--------------|------------:|------------:|------------:|
| coal-st       |      8100   |      4000   |         0   |
| gas-ccgt      |     23400   |     30000   |     13000   |
| gas-ocgt      |     10000   |         0   |         0   |
| hydro-ror     |      3993.6 |      3993.6 |      3993.6 |
| lignite-st    |      9000   |      5000   |         0   |
| mixed-st      |      4100   |      4100   |      2000   |
| oil-ocgt      |       900   |       450   |         0   |
| solar-pv      |    104500   |    127250   |    150000   |
| wind-offshore |     17000   |     26000   |     35000   |
| wind-onshore  |     85500   |    105250   |    125000   |

### Efficiencies

| carrier   | tech     | 2030   | 2040    | 2050   |
|:----------|:---------|:-------|:--------|:-------|
| biomass   | st       | 0.35   | 0.4185  | 0.487  |
| coal      | st       | 0.4    | 0.425   | 0.45   |
| gas       | ccgt     | 0.5    | 0.53475 | 0.5695 |
| gas       | ocgt     | 0.38   | 0.373   | 0.366  |
| hydro     | phs      | 0.75   | 0.75    | 0.75   |
| hydro     | ror      | 0.9    | 0.9     | 0.9    |
| hydro     | rsv      | 0.9    | 0.9     | 0.9    |
| lignite   | st       | 0.4    | 0.4     | 0.4    |
| oil       | ocgt     | 0.35   | 0.373   | 0.396  |
| uranium   | st       | 0.33   | 0.335   | 0.34   |
| waste     | st       | 0.26   | 0.26    | 0.26   |
| mixed     | st       | 0.26   | 0.28    | 0.3    |
| lithium   | battery  | 0.85   | 0.885   | 0.92   |
| air       | caes     | 0.57   | 0.57    | 0.57   |
| wind      | onshore  | NA     | NA      | NA     |
| wind      | offshore | NA     | NA      | NA     |
| solar     | pv       | NA     | NA      | NA     |

### Cost

| scenario   | carrier   |   value | unit    | source         |
|:-----------|:----------|--------:|:--------|:---------------|
| 2030C      | biomass   |  27.29  | EUR/MWh | Prognos2013    |
| 2030C      | co2       |  29.4   | EUR/t   | NEP2019        |
| 2030C      | coal      |   8.4   | EUR/MWh | NEP2019        |
| 2030C      | gas       |  26.4   | EUR/MWh | NEP2019        |
| 2030C      | lignite   |   5.6   | EUR/MWh | NEP2019        |
| 2030C      | mixed     |   6.7   | EUR/MWh | Own Assumption |
| 2030C      | oil       |  48.3   | EUR/MWh | NEP2019        |
| 2030C      | uranium   |   1.692 | EUR/MWh | TYNDP2018      |
| 2030C      | waste     |   6.7   | EUR/MWh | IRENA2015      |
| 2040GCA    | biomass   |  40     | EUR/MWh | Own Assumption |
| 2040GCA    | co2       | 126     | EUR/t   | TYNDP2018      |
| 2040GCA    | coal      |   6.48  | EUR/MWh | TYNDP2018      |
| 2040GCA    | gas       |  30.24  | EUR/MWh | TYNDP2018      |
| 2040GCA    | lignite   |   3.96  | EUR/MWh | TYNDP2018      |
| 2040GCA    | mixed     |   6.7   | EUR/MWh | Own Assumption |
| 2040GCA    | oil       |  50.22  | EUR/MWh | TYNDP2018      |
| 2040GCA    | uranium   |   1.692 | EUR/MWh | TYNDP2018      |
| 2040GCA    | waste     |   6.7   | EUR/MWh | Own Assumption |
| 2050-100RE | biomass   |  50     | EUR/MWh | Own Assumption |
| 2050-100RE | co2       | 150     | EUR/t   | Own Assumption |
| 2050-100RE | coal      |   8     | EUR/MWh | Own Assumption |
| 2050-100RE | gas       |  54     | EUR/MWh | Own Assumption |
| 2050-100RE | lignite   |   6     | EUR/MWh | Own Assumption |
| 2050-100RE | mixed     |   6.7   | EUR/MWh | Own Assumption |
| 2050-100RE | oil       |  60     | EUR/MWh | Own Assumption |
| 2050-100RE | uranium   |   1.692 | EUR/MWh | Own Assumption |
| 2050-100RE | waste     |  30     | EUR/MWh | Own Assumption |


## All capacities

|    |   coal-st |   gas-ccgt |   gas-ocgt |   hydro-ror |   lignite-st |   mixed-st |   oil-ocgt |   solar-pv |   uranium-st |   wind-offshore |   wind-onshore |
|:---|----------:|-----------:|-----------:|------------:|-------------:|-----------:|-----------:|-----------:|-------------:|----------------:|---------------:|
| AT |         0 |          0 |       2969 |        5566 |            0 |        984 |        174 |       5600 |            0 |               0 |           5500 |
| BE |         0 |          0 |       4956 |          10 |            0 |       1710 |          0 |      22000 |            0 |            8300 |           7700 |
| CH |         0 |          0 |          0 |         385 |            0 |        985 |          0 |      12600 |            0 |               0 |           2590 |
| CZ |       251 |          0 |        995 |         150 |         1297 |       1505 |        180 |       5230 |         3277 |               0 |           1330 |
| DE |      4000 |      30000 |          0 |        3994 |         5000 |       4100 |        450 |     127250 |            0 |           26000 |         105250 |
| DK |         0 |          0 |          0 |           0 |            0 |         99 |        337 |       7453 |            0 |            7807 |           7180 |
| FR |         0 |          0 |       8892 |       10243 |            0 |          0 |        990 |      60000 |        37640 |           20000 |          49050 |
| IT |      4759 |          0 |      30734 |        5720 |            0 |       5785 |       3337 |      58271 |            0 |           11437 |          17785 |
| NL |      3358 |          0 |       7593 |           0 |            0 |       3539 |          0 |      46000 |            0 |           23433 |           7400 |
| NO |         0 |          0 |          0 |        2211 |            0 |          0 |          0 |       3000 |            0 |             400 |          10036 |
| PL |      8326 |          0 |       2741 |         708 |         1936 |       7276 |       3945 |      42507 |         7500 |            7000 |          32927 |
| SE |         0 |          0 |          0 |        6520 |            0 |        390 |          0 |       6703 |         3682 |            1303 |          17418 |

|    |   coal-st |   gas-ccgt |   lignite-st |   mixed-st |   oil-ocgt |   gas-ocgt |   hydro-ror |   solar-pv |   wind-offshore |   wind-onshore |
|:---|----------:|-----------:|-------------:|-----------:|-----------:|-----------:|------------:|-----------:|----------------:|---------------:|
| AT |         0 |          0 |            0 |          0 |          0 |       1500 |        5566 |      12090 |               0 |           6880 |
| BE |         0 |          0 |            0 |          0 |          0 |       2500 |          10 |      24087 |            3000 |          10903 |
| CH |         0 |          0 |            0 |          0 |          0 |       2000 |         385 |      15000 |               0 |           1382 |
| CZ |         0 |          0 |            0 |          0 |          0 |       1750 |         150 |      13048 |               0 |          10234 |
| DE |         0 |      13000 |            0 |       2000 |          0 |          0 |        3994 |     150000 |           35000 |         125000 |
| DK |         0 |          0 |            0 |          0 |          0 |       1000 |           0 |       2038 |           25600 |          18708 |
| FR |         0 |          0 |            0 |          0 |          0 |      16000 |       10243 |     103055 |               0 |         124197 |
| IT |         0 |          0 |            0 |          0 |          0 |       9000 |        5720 |      91415 |               0 |          41290 |
| NL |         0 |          0 |            0 |          0 |          0 |       3000 |           0 |      22247 |           15900 |          14997 |
| NO |         0 |          0 |            0 |          0 |          0 |          0 |        2211 |       5364 |            3000 |          12175 |
| PL |         0 |          0 |            0 |          0 |          0 |       3000 |         708 |      24220 |               0 |          81918 |
| SE |         0 |          0 |            0 |          0 |          0 |          0 |        6520 |       8919 |            3000 |          24211 |

|    |   coal-st |   gas-ccgt |   gas-ocgt |   hydro-ror |   lignite-st |   mixed-st |   oil-ocgt |   solar-pv |   uranium-st |   wind-offshore |   wind-onshore |
|:---|----------:|-----------:|-----------:|------------:|-------------:|-----------:|-----------:|-----------:|-------------:|----------------:|---------------:|
| AT |         0 |          0 |       3928 |        5566 |            0 |        984 |        174 |       7803 |            0 |               0 |           5000 |
| BE |         0 |          0 |       6352 |          10 |            0 |       1157 |        500 |       6851 |            0 |            2310 |           3298 |
| CH |         0 |          0 |          0 |         385 |            0 |        985 |          0 |       9371 |         1190 |               0 |            370 |
| CZ |         0 |          0 |        995 |         150 |         4760 |       1505 |          0 |       6993 |         4055 |               0 |            950 |
| DE |      8100 |      23400 |      10000 |        3994 |         9000 |       4100 |        900 |     104500 |            0 |           17000 |          85500 |
| DK |       410 |          0 |          0 |           0 |            0 |         99 |        817 |       5113 |            0 |            2905 |           5596 |
| FR |         0 |          0 |       8892 |       10243 |            0 |          0 |       6424 |      41600 |        37640 |            7000 |          36336 |
| IT |      2811 |          0 |      32705 |        5720 |            0 |       5785 |        354 |      46386 |            0 |             654 |          15575 |
| NL |      4608 |          0 |       7593 |           0 |            0 |       3539 |          0 |      14084 |          486 |           11500 |           6723 |
| NO |         0 |          0 |        435 |        2211 |            0 |          0 |          0 |       2972 |            0 |               0 |           3330 |
| PL |     13771 |          0 |       2741 |         708 |         7405 |       7276 |       1000 |      24870 |         3000 |            2250 |           9200 |
| SE |         0 |          0 |          0 |        6520 |            0 |        390 |          0 |       5384 |         6852 |             190 |          10780 |


# Data Sources

* [TYNDP2018a](https://www.entsoe.eu/Documents/TYNDP%20documents/TYNDP2018/Scenarios%20Data%20Sets/Input%20Data.xlsx)
* [TYNDP2018b](https://www.entsoe.eu/Documents/TYNDP%20documents/TYNDP2018/Scenarios%20Data%20Sets/ENTSO%20Scenario%202018%20Generation%20Capacities.xlsm)
* [NinjaWind](https://www.renewables.ninja/static/downloads/ninja_europe_wind_v1.1.zip)
* [NinjaPV](https://www.renewables.ninja/static/downloads/ninja_europe_pv_v1.1.zip)
* [OPSDa](https://data.open-power-system-data.org/time_series/2018-06-30/time_series_60min_singleindex.csv)
* [OPSDb](https://data.open-power-system-data.org/conventional_power_plants/2018-12-20/conventional_power_plants_DE.csv)
* [OPSDc]("https://data.open-power-system-data.org/when2heat/opsd-when2heat-2019-08-06.zip")
* [NEP2019a](https://www.netzentwicklungsplan.de/sites/default/files/paragraphs-files/NEP_2030_V2019_2_Entwurf_Teil1.pdf)
* [NEP2019b](https://www.netzentwicklungsplan.de/sites/default/files/paragraphs-files/Kraftwerksliste_%C3%9CNB_Entwurf_Szenariorahmen_2030_V2019_0_0.xlsx)
* [Restore2050](https://zenodo.org/record/804244/#.XTcUhfyxUax)
* [Brown](https://zenodo.org/record/1146666#.XTcTdvyxUaw)
* [ANGUS](https://github.com/ZNES-datapackages/angus-input-data)
* [hotmaps](https://gitlab.com/hotmaps/potential/potential_biomass)
