
# ANGUS II Scenario description


## Overview

The developed scenarios are based on the TYNDP2018, the NEP2019, the e-Highway 100%RES
scenario and the UBA RESCUE scenarios.

For the non-german countries the following data has been used:

* 2030: TYNDP2018 DG (distributed generation vision)
* 2040: TYNDP2018 2040 GCA (global climate action vision)
* 2050: E-Highway 100% RES

The e-Highway2050 [ehighway]  has been funded by the European Commission.
The project aimed develop
a plan for the European transmission network from 2020 to 2050. One important
part of this study is the support of EU’s overall policy objectives
with regard to energy. The study is builds upon the TYNDP2016 and includes
scenarios for 100% renewable energy supply in 2050. The TYNDP is developed
by the network of European TSO (ENTSOE), therefore it also plays an important
role for the NEP which is developed by the four german TSO.

For Germany the starting point for the pathyways is the NEP2019:

 * 2030: NEP 2019 C
 * 2040: Interpolated (TYNDP2018)
 * 2050: RESCUE, E-Highway

The scenarios from literature and their different visions have been selected
to model a pathway towards 100% renewable energy system in Germany to
adhere to the COP paris agreement. As the e-Highway scenarios are based on the
TYNDP2016 and the NEP2019 is aligned with the TYNDP2018, the scenario for
the year 2050 has been adapted for the focus country of Germany.

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

| name          |   ANGUS2030 |   ANGUS2040 |   ANGUS2050 |
|:--------------|------------:|------------:|------------:|
| coal-st       |        8100 |        4000 |           0 |
| gas-ccgt      |       23400 |       30000 |       13000 |
| gas-ocgt      |       10000 |           0 |           0 |
| lignite-st    |        9000 |        5000 |           0 |
| mixed-st      |        4100 |        4100 |        2000 |
| oil-ocgt      |         900 |         450 |           0 |
| solar-pv      |      104500 |      127250 |      150000 |
| wind-offshore |       17000 |       26000 |       35000 |
| wind-onshore  |       85500 |      105250 |      125000 |


In the TYNDP2018 and Ehighway scenario gas fired power plants are not seperated
into CCGT and OCGT. Therefore a factor of 0.5 [ISE2011] is used to split the
total gas capacity into these to technologies.

### Conventional energies

Efficiencies and commodity costs are based on the TYNDP2018 and the NEP2030C for
2030. The availability factor (avf) of technologies and variable
operation and maintenance cost (vom) are the same for all scenarios.
The avf is based on the PRIMES model assumptions.[PRIMES2016] For detailed data
see Annex I.

### Renewable Energies

For the renewable profiles of wind and pv timeseries of renewables ninja has
been used. The maximum biomass potential per country the hotmaps potential is used.

Hydro data is based on the TYNDP2018 GCA (global climate action) vision.
However it should be noted, that due to the low cost and the limited potential
of hydro power, the installed capacities within the vision and years of the TYNDP
do not differ significantly.

* The reservoir (rsv) capacity is calculated by substracting the column 'hydro-pump
from column 'hydro turbine' in the original data source. Therefore, it is assumed,
that each pumped hydro storage (phs) have equal pump/turbine capacities.
* The max-hours for phs is based on Geth et al. 2018.
* The max-hours for rsv is calculated for each country based on the Restore2050 data, where
rsv storage capacity in TWh is provided in addition to the installed capacity.
It is assumed that  new rsv plants will have the same reservoir sizes in
each country as provided in current data from the Restore2050 project.

The inflow in run of river and reservoirs is modelled based on the inflow timeseries
of the Restore2050 project.

## Grid

The grid for 2030 and 2040 is based on the TYNDP2018, while the grid for 2050
is based on the e-Highway 100% RES scenario.

![Installed tranmission capacities in 2030](grid-scenarioANGUS2030.pdf)

![Installed tranmission capacities in 2040](grid-scenarioANGUS2040.pdf)

![Installed tranmission capacities in 2050](grid-scenarioANGUS2050.pdf)

## Annex I


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




# Data Sources

* [ehighway](https://www.entsoe.eu/outlooks/ehighways-2050/)
* [PRIMES2016](https://ec.europa.eu/energy/sites/ener/files/documents/metis_technical_note_t1_-_integration_of_primes_scenarios_into_metis.pdf)
* [ISE2011](https://www.isi.fraunhofer.de/content/dam/isi/dokumente/ccx/2011/Final_Report_EU-Long-term-scenarios-2050.pdf)
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
