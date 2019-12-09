
# Scenarios


## Existing Scenarios

* NEP and Ehighway
* others ?


## Assumptions

### Spatial and temporal resolution

**Assumptions**: The scenarios model the western europe energy system with one
node per country, i.e. reflecting the market zones. Countries modelled are:
**AT, BE, CH, CZ, DE, DK, FR, IT, NL, NO, PL, SE.**
 The model simulates the the system on an hourly basis for one year using a
 perfect foresight approach. The modelled years are: 2030 and 2050.

**Implications & Limitations**: Intra-country grid constraints are not
reflected by the model. Hence, renwable energy  curtailment and/or storage
demand may be underestimated.

## Demand

* Demand profiles are calculated from the OPSD dataset of the ENTSOE
timeseries for the selected weather year (2012).
* German demand for 2030 is based on the NEP2030 scenario 2030C
* The amount of demand of the neigbouring countries is based on the TYNDP2018
scenario for 2030 'Sustainable Transition'. (For the NEP2030C, the TYNDP
*Vision 2030 DG* has been chosen, for NEP2030A *VisionEU* has been used)
* The demand for 2050 is based on the E-Highway demand calculations.


## Conventional generation

For Germany the installed capacities from the
NEPScenario 2019 C are implemented. The capacities generation of german
neigbouring countries are based on the  *Vision 2030DG* of the TYNDP2018. 2050
capacities are derived from the E-Highway scenario *100% RE*.

![Installed Capacities](installed_capacities.pdf)

* Efficiencies are based on own assumptions for non-german countries. However,
the data of the TYNDP2018 has been used as a foundation.

| carrier   | tech     |   2030 | 2050   |
|:----------|:---------|-------:|:-------|
| biomass   | ce       |   0.35 | 0.35   |
| biomass   | st       |   0.35 | 0.487  |
| coal      | st       |   0.4  | 0.45   |
| coal      | ccgt     |   0.4  | NA     |
| gas       | ccgt     |   0.5  | 56.95  |
| gas       | ocgt     |   0.38 | 36.6   |
| gas       | st       |   0.36 | 41.7   |
| gas       | gt       |   0.4  | 33.6   |
| hydro     | phs      |   0.75 | 0.75   |
| hydro     | ror      |   0.9  | 0.9    |
| hydro     | rsv      |   0.9  | 0.9    |
| lignite   | st       |   0.4  | 0.4    |
| oil       | ocgt     |   0.35 | 0.396  |
| oil       | st       |   0.35 | 41     |
| uranium   | st       |   0.33 | 34.3   |
| waste     | chp      |   0.26 | 0.3    |
| waste     | industry |   0.26 | NA     |
| mixed     | gt       |   0.26 | 0.3    |
| lithium   | battery  |   0.85 | 0.92   |
| air       | caes     |   0.57 | 0.57   |




For germany the OPSD powerplant register is used to calculate efficiencies for
the conventional powerplants in 2030.

* Costs are based on the NEP2030C and TYNDP2018 cost assumptions:

| scenario   | carrier   |   value | unit    | source         |
|:-----------|:----------|--------:|:--------|:---------------|
| 2030C      | biomass   |  27.29  | EUR/MWh | Prognos2013    |
| 2030C      | co2       |  29.4   | EUR/t   | NEP2019        |
| 2030C      | coal      |   8.4   | EUR/MWh | NEP2019        |
| 2030C      | gas       |  26.4   | EUR/MWh | NEP2019        |
| 2030C      | lignite   |   5.6   | EUR/MWh | NEP2019        |
| 2030C      | oil       |  48.3   | EUR/MWh | NEP2019        |
| 2030C      | uranium   |   1.692 | EUR/MWh | TYNDP2016A     |
| 2030C      | waste     |   6.7   | EUR/MWh | IRENA2015      |
| 2050-100RE | biomass   |  30     | EUR/MWh | Own Assumption |
| 2050-100RE | co2       | 150     | EUR/t   | Own Assumption |
| 2050-100RE | coal      |   8     | EUR/MWh | Own Assumption |
| 2050-100RE | gas       |  54     | EUR/MWh | Own Assumption |
| 2050-100RE | lignite   |   6     | EUR/MWh | Own Assumption |
| 2050-100RE | oil       |  60     | EUR/MWh | Own Assumption |
| 2050-100RE | uranium   |   1.5   | EUR/MWh | Own Assumption |
| 2050-100RE | waste     |  30     | EUR/MWh | Own Assumption |
| climate    | biomass   |  27.29  | EUR/MWh | Prognos2013    |
| climate    | co2       | 100     | EUR/t   | Own Assumption |
| climate    | coal      |   8.4   | EUR/MWh | NEP2019        |
| climate    | gas       |  26.4   | EUR/MWh | NEP2019        |
| climate    | lignite   |   5.6   | EUR/MWh | NEP2019        |
| climate    | oil       |  48.3   | EUR/MWh | NEP2019        |
| climate    | uranium   |   1.692 | EUR/MWh | TYNDP2016A     |
| climate    | waste     |   6.7   | EUR/MWh | IRENA2015      |


## Renewables

* Maximum biomass potential per country the hotmaps potential is used. The
installed capacity of biomass is assumed to be `biofuels` and `others-res`
from the TNYDP2018.
* Renewable capacities for wind and pv are based on the TYNDP2018 for non german
countries.
* For the renewable profiles of wind and pv timeseries of renewables ninja has
been used.
* Hydro reservoir and run of river capacities are assumend to be the same as in 2015. The inflow in run of river and
reservoirs is modelled based on the inflow timeseries of the Restore2050 project.
* Pumped hydro capacity differs among the scenarios.

## Must Run

* For the NEP2030C scenario, CHP power plants smaller 10MW are modelled as must-run
with a seasonal profile.
* For the NEP2030A scenario, > 30 GW installed conventional powerplants are must
run with the seasonal profile.
* Must run plants are modelled with marginal cost of zero.



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
