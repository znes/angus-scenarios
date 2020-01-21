---
title: ANGUS II Scenario Description
author: Simon Hilpert and Clemens Wingenbach
date: January, 2020
header: This is fancy
footer: So is this
geometry: margin=2.5cm
abstract:

header-includes: |
    \usepackage{graphicx}
    \usepackage{caption}
    \usepackage{subcaption}
---

# Background

The ANGUS scenarios and their assumptions have been developed
to model a pathway towards 100% renewable energy system in Germany. The assessed
system aims to adhere with the COP Paris agreement, i.e. providing a CO2-neutral
energy supply in Germany. The developed scenarios are based on the TYNDP2018,
the NEP2019, the
e-Highway 100%-RES scenario and the UBA RESCUE scenarios. Their main purpose
is to generate storage operation profiles (power, energy) to assess underground storage
technologies with regard to techno-ecnomic indicators. Therefore, the
shadow prices of the developed techno-economic energy system model play an
important role as economic signal for the storage dispatch and the model coupling
(see ANGUS Case Studies). Hence, high priority is given to sensitivities that have a
major effect on the storage dispatch and requirements of the future German
energy system. The German energy system is modelled with greater detail as the
neighbouring countries due to the regional focus of this study.

## Existing Scenarios
The *Netzentwicklungsplan (NEP)* is developed by the German transmission system
operator (TSOs) to plan the
transmission grid in Germany. The NEP is based on a broad public consultation
phase to enable high acceptance of planned grid expansion. Similarly, the Ten Year
Netwok Development Plan
(TYNDP) is developed by the European TSOs with regard to the European grid.
The process of the national NEP and the TYNDP is aligned to ensure coherent national
and international planning.  The scenarios in both of these plans reflect current
and expected socio-economic developments as well as relevant policy decisions.
Due to the public consultation and their prominent nature, these scenarios constitute
import visions for the future European energy system. However, both plans are
focussing on the short to mid-term perspective. Therefore, within the ANGUS project
another prominent scenario development project, the e-Highway2050 project, is
used as a foundation for the  scenario development.
The e-Highway2050 project has been funded by the European Commission.
The project aimed to develop a plan for the European transmission network from 2020
to 2050. One important part of this study is the support of EU’s overall policy
objectives with regard to energy. The study builds upon the TYNDP2016 and
includes scenarios for 100% renewable energy supply in 2050. The TYNDP is developed
by the network of European TSO (ENTSOE), therefore it also plays an important
role for the NEP which is developed by the four German TSOs.

\newpage
In literature different scenarios for 100% renewable energy systems can found.
Figure \ref{scenario-comparison} shows installed capacities of renewable energies
in Germany for systems with high share of renewables.
One important factor for the required capacity / energy is the future electricity
demand including the electrification of heat and transport sectors. In addition,
capacity factors and biomass potentials are crucial aspects. While PV
capacity factors lie within a small range of values, onshore and offshore
capacity factors can vary strongly with major impacts on results. While in the
BMWI Reference scenario onshore wind fullloadhours (flh) are 3527 (capacity factor of 0.403),
the onshore wind production in e-Highway 100% RES scenario is modelled with 2102
flh (average capacitiy factor of 0.24). However, the avaible biomass potential
can be considered to be even more imporant, as it constitutes the only dispatchable
renewable energy source.

![Installed renewable capacities in scenarios from literature\label{scenario-comparison}](scenario-comparison.pdf)

The lowest capacities are found in the BMWI Reference scenario. However, capacity
factors
for wind in the scenario are significantly higher compared to the other scenarios.
In addition, this scenario only comes with a share of approx. 82% RE.
The highest capacities wind and pv are obtained in the RESCUE GL scenario. Here
the 100% RE, no import and the higher demand of 796 TWh are the driving factors.
Within the set of scenarios, the wind and pv capacities of e-Highway scenario are
rather located at the lower end of the range. The main reason is the high biomass
potential, increasing hydro capacities ( in particular in Norway) and higher
offshore wind. This results in significant imports in Germany, but also lower
installed capacities of onshore wind and pv. In addtion to the before mentioned
factors, system flexibility is another important determinate. Here grid
infrastructure (regional flexibility) and storages (temporal flexbiliy) have to
be considered.


# Scenario Assumptions

## Spatial and temporal resolution

**Assumptions**: The scenarios model the Western European energy system with one
node per country. Countries modelled are:
**AT, BE, CH, CZ, DE, DK, FR, IT, LU, NL, NO, PL, SE.**
 The model simulates the system on an hourly basis for one year using a
 perfect foresight approach with the years 2030 and 2050.

**Implications & Limitations**: Intra-country grid constraints are not
reflected by the model. Hence, renewable energy curtailment and/or storage
demand may be underestimated.

## Grid

The grid for 2030 and 2040 is based on the TYNDP2018 (see Annex), while the grid for
2050 is based on the e-Highway 100% RES scenario. Figure \ref{grid_2050} shows
the installed transmission capacities of the 2050 electricity system. The transmission
system is modelled with a transshipment approach assuming a loss of 0.03 on the lines.

![Installed transmission capacities in 2050.\label{grid_2050}](grid-scenarioANGUS2050.pdf){width=60%}


## Demand

### Conventional electricity demand
The German goals regarding efficiency aim to reduce the electricity demand
by 10% until 2020 and 25% by 2050 compared to 2008 levels (403.8 TWh). 
The development of future electricity demand strongly depends on demographic and
economic development as well as implemented efficiency measures.
In literature, different values can be found. Assumptions regarding the
electricity demand are an important driving factor for the energy system.
At the same time, these values come with a high degree of uncertainty
(Result of the ANGUS Scenario Workshop). While the conventional electricity demand
within the *Basis Szenario* of the German *Langfristszenarien* accounts for
441.2 TWh in 2030 and 417.2 TWh in 2050 respectively, the demand in the NEP2019
scenarios for 2030 is slightly higher (477 TWh).

### Sector coupling
Despite a decreasing demand due to efficiency measures, the electrification
of other sectors (heat, transport) will create an additional demand for electricity.
Currently the heat demand for residential heating accounts for 122.4 TWh hot water
and 678.5 TWh space heating (2017). The German government set a goal of 60-80%
reduction for this sector 2050. These values are very ambitious, as current
values of insulation are lacking behind necessary rates. Heat demand in the
RESCUE scenarios ranges from 436.8 TWh (green late scenario: GL) to 246.2 TWh
(green supreme scenario: GS). These amounts
 correspond to a reduction of approx. 72 % to 50 % compared to 2008 (889 TWh).
The supply for this heat demand is heavily based on electricity (heatpumps) with 74.6 %
(GS) and 65 % (GL). The remaining energy is provided by district heating (62.4 TWh,
 GS) and in the case of the GL also by additional local gas boilers.

In the NEP2019 2030C scenario, additional 29 TWh electricity from heatpumps in
residential heating and 25 TWh additional demand for electric vehicles are consumed.
In contrast, within the BMWI scenarios, 17.8 TWh electricity for
heatpumps is consumed. These values are in the range with the RESCUE green
late (GL) and green supreme (GS) scenarios with 57 TWh_th and 95 TWh_th respectively
(assuming an coefficienct of performance of approximately 3). Therefore, for 2050  both RESCUE
scenarios are used as a basis for additional electricity demand due to space heating.

Demand profiles are calculated from the OPSD dataset of the ENTSOE
timeseries for the selected weather year (2012).


*Implications & Limitations*:

* Due to the historic demand profiles, future
flexibilities like smart operation of certain applications and industry
processes are not modelled.
* The model only covers the residential hot water and space heating demand.
*Electric vehicles are modelled without specific profile for charging / discharging but only
with a constant additional base load.



## Generation capacity

The different scenarios are based on the NEP2019, TYNDP2018 and the e-Highway
project.

* NEP2030C: Installed capacities in Germany are based on the NEP2019 scenario 2030C. The
capacities of neighbouring countries are based on the TYNDP2018-2030ST vision. The
renewable share of produced energy in Germany in this scenario is approx. 68 %.
* 2040GCA: This scenario is based on the TYNDP2018-GCA vision.
* 2050ZNES: The base scenario is the e-Highway 100 % RES scenario. This scenario
strongly depends on hydro capacity expansion in Norway and also substantial biomass
capacity/energy. Based on the input data, this scenario has an renewable
energy supply share of approx. 95 % .
* 2050ANGUS: Therefore, the adapted ANGUS scenarios haven been developed to
describe 100% renewable energy scenarios with different sensitivities such
as the no-biomass (nb).

The installed capacities in Germany are shown in the Figure \ref{installed_capacities}
below.

![Installed generation capacity in Germany in 2050.\label{installed_capacities}](installed_capacities.pdf){width=100%}

Note that only the scenarios 2030NEPC, 2040GCA, 2050ANGUS-(nb) depict a path towards
100% renewable energy supply.

## Renewable Energies

For 2030 and 2040 the reservoir data has been calculated as follows:

* The reservoir (rsv) capacity is calculated by subtracting the column 'hydro-pump
from column 'hydro turbine' in the original data source. Therefore, it is assumed,
that each pumped hydro storage (phs) has equal pump/turbine capacities.
* The max-hours (energy capacity) for phs is based on Geth et al. 2018.
* The max-hours for rsv is calculated for each country based on the Restore2050
data, where rsv storage capacity in TWh is provided in addition to the installed capacity.
It is assumed that all new rsv plants will have the same reservoir sizes in
each country as provided in current data from the Restore2050 project.

Onshore wind and pv timeseries are based on renewables ninja for each country.
The offshore profiles are taken from the Vernetzen-project and adapted with a
correction factor of 0.8 which has been derived from the energy production in
the e-Highway scenarios. The inflow in run of river and reservoirs is modelled
with the inflow timeseries of the Restore2050 project.

Full load hours of renewable energy technologies:

| country   |   offshore |   onshore |   pv |   ror |
|:----------|-----------:|----------:|-----:|------:|
| AT        |        nan |      1507 | 1291 |  2038 |
| BE        |       3939 |      2406 | 1135 |   890 |
| CH        |        nan |      1354 | 1416 |  2555 |
| CZ        |        nan |      1875 | 1226 |  1316 |
| DE        |       3976 |      1951 | 1151 |  3082 |
| DK        |       4224 |      2670 |  977 |     0 |
| FR        |       3295 |      2040 | 1265 |  1815 |
| LU        |        nan |      2917 | 1192 |  1947 |
| NL        |       4025 |      1921 | 1095 |  1012 |
| NO        |       4341 |      3562 |  811 |  2028 |
| PL        |       3964 |      1834 | 1113 |   995 |
| SE        |       3792 |      2654 |  862 |  2161 |


The maximum biomass potential per country is derived from the [hotmaps] project
and is equal for all scenarios in the ANGUS project. The potential does not cover
waste but only agriculture and forestry residues. With an efficiency of 0.487
for biomass to electricity conversion the potential in Germany is approx.
73 TWh_el.

Biomass potential:

|    | Amount in TWh |
|:---|-----------:|
| AT |  23.6111   |
| BE |   8.08333  |
| CH |   0        |
| CZ |  32.7778   |
| DE | 150.167    |
| DK |  13.5556   |
| FR | 149.556    |
| LU |   0.611111 |
| NL |   2.80556  |
| NO |   0        |
| PL |  71.3611   |
| SE |  86.75     |



# Annex I

## Hydro data

| country   |   year |      rsv |      phs |        ror |   ror-share |   phs-max-hours |   rsv-max-hours |
|:----------|-------:|---------:|---------:|-----------:|------------:|----------------:|----------------:|
| AT        |   2030 |  4787.52 |  6055.33 |  4671.9    |    0.493889 |              33 |             857 |
| AT        |   2040 |  4787.52 |  6055.33 |  4671.9    |    0.493889 |              33 |             857 |
| AT        |   2050 |  5676    | 10733    |  7401.16   |    0.565961 |              33 |             857 |
| BE        |   2030 |   158    |  1150    |   117      |    0.425455 |               4 |             500 |
| BE        |   2040 |   158    |  1908    |   117      |    0.425455 |               4 |             500 |
| BE        |   2050 |     0    |  2308    |   331.972  |    1        |               4 |             500 |
| CH        |   2030 |  8987    |  4593    |  4139      |    0.315328 |             136 |             906 |
| CH        |   2040 |  8987    |  6722    |  4139      |    0.315328 |             136 |             906 |
| CH        |   2050 |  8130    |  5443    |  4122.7    |    0.336473 |             136 |             906 |
| CZ        |   2030 |    50    |  1000    |   365      |    0.879518 |               5 |            1111 |
| CZ        |   2040 |    50    |  1145    |   365      |    0.879518 |               5 |            1111 |
| CZ        |   2050 |   819    |  1787    |   454.846  |    0.357065 |               5 |            1111 |
| DE        |   2030 |   995.9  |  9791.6  |  4329      |    0.812973 |               6 |             592 |
| DE        |   2040 |   620    | 10244    |  4329      |    0.874722 |               6 |             592 |
| DE        |   2050 |   620    | 12799    |  4233      |    0.872244 |               6 |             592 |
| DK        |   2030 |     0    |     0    |     6.6082 |    1        |               6 |                 |
| DK        |   2040 |     0    |     0    |     6.6082 |    1        |               6 |                 |
| DK        |   2050 |     0    |     0    |    13.3102 |    1        |               6 |                 |
| FR        |   2030 |  8197    |  5500    | 13797      |    0.627307 |              15 |            1201 |
| FR        |   2040 |  8000    |  5500    | 13600      |    0.62963  |              15 |            1201 |
| FR        |   2050 | 18200    | 13420    | 10318.6    |    0.36182  |              15 |            1201 |
| LU        |   2030 |   284    |  1026    |    34      |    0.106918 |               4 |            2840 |
| LU        |   2040 |   284    |  1026    |    34      |    0.106918 |               4 |            2840 |
| LU        |   2050 |     0    |  1650.68 |   149.203  |    1        |               4 |            2840 |
| NL        |   2030 |     0    |     0    |    38      |    1        |               6 |                 |
| NL        |   2040 |     0    |  2500    |    38      |    1        |               6 |                 |
| NL        |   2050 |     0    |     0    |   104.435  |    1        |               6 |                 |
| NO        |   2030 | 34702.2  |  1114.71 |     0      |    0        |             314 |            3139 |
| NO        |   2040 | 34702.2  |  1114.71 |     0      |    0        |             314 |            3139 |
| NO        |   2050 | 42473    | 17291    | 28141      |    0.398518 |             314 |            3139 |
| PL        |   2030 |     0    |  1488    |  1033      |    1        |               5 |            5477 |
| PL        |   2040 |     0    |  2292    |  1033      |    1        |               5 |            5477 |
| PL        |   2050 |     0    |  3790    |  2078.8    |    1        |               5 |            5477 |
| SE        |   2030 | 16184    |     0    |     0      |    0        |             793 |            3456 |
| SE        |   2040 | 16184    |     0    |     0      |    0        |             793 |            3456 |
| SE        |   2050 | 21383.3  |     0    | 10775.2    |    0.335066 |             793 |            3456 |


## Carrier cost

| scenario   | carrier   |   value | unit    | source         |
|:-----------|:----------|--------:|:--------|:---------------|
| 2030DG     | biomass   |  30.32  | EUR/MWh | HeatRoadMap    |
| 2030DG     | co2       |  50     | EUR/t   | TYNDP2018      |
| 2030DG     | coal      |   9.72  | EUR/MWh | TYNDP2018      |
| 2030DG     | gas       |  31.68  | EUR/MWh | TYNDP2018      |
| 2030DG     | lignite   |   3.96  | EUR/MWh | TYNDP2018      |
| 2030DG     | mixed     |   6.7   | EUR/MWh | Own Assumption |
| 2030DG     | oil       |  78.48  | EUR/MWh | TYNDP2018      |
| 2030DG     | uranium   |   1.692 | EUR/MWh | TYNDP2018      |
| 2030DG     | waste     |   6.7   | EUR/MWh | Own Assumption |
| 2030NEPC   | biomass   |   5     | EUR/MWh | Own Assumption |
| 2030NEPC   | co2       |  29.4   | EUR/t   | NEP2019        |
| 2030NEPC   | coal      |   8.4   | EUR/MWh | NEP2019        |
| 2030NEPC   | gas       |  26.4   | EUR/MWh | NEP2019        |
| 2030NEPC   | lignite   |   5.6   | EUR/MWh | NEP2019        |
| 2030NEPC   | mixed     |   6.7   | EUR/MWh | Own Assumption |
| 2030NEPC   | oil       |  48.3   | EUR/MWh | NEP2019        |
| 2030NEPC   | uranium   |   1.692 | EUR/MWh | TYNDP2018      |
| 2030NEPC   | waste     |   6.7   | EUR/MWh | IRENA2015      |
| 2040GCA    | biomass   |  30.32  | EUR/MWh | HeatRoadMap    |
| 2040GCA    | co2       | 126     | EUR/t   | TYNDP2018      |
| 2040GCA    | coal      |   6.48  | EUR/MWh | TYNDP2018      |
| 2040GCA    | gas       |  30.24  | EUR/MWh | TYNDP2018      |
| 2040GCA    | lignite   |   3.96  | EUR/MWh | TYNDP2018      |
| 2040GCA    | mixed     |   6.7   | EUR/MWh | Own Assumption |
| 2040GCA    | oil       |  50.22  | EUR/MWh | TYNDP2018      |
| 2040GCA    | uranium   |   1.692 | EUR/MWh | TYNDP2018      |
| 2040GCA    | waste     |   6.7   | EUR/MWh | Own Assumption |
| 2050ZNES   | biomass   |  34.89  | EUR/MWh | HeatRoadMap    |
| 2050ZNES   | co2       | 150     | EUR/t   | Own Assumption |
| 2050ZNES   | coal      |   7.97  | EUR/MWh | HeatRoadMap    |
| 2050ZNES   | gas       |  43.72  | EUR/MWh | HeatRoadMap    |
| 2050ZNES   | lignite   |   6     | EUR/MWh | Own Assumption |
| 2050ZNES   | mixed     |   6.7   | EUR/MWh | Own Assumption |
| 2050ZNES   | oil       |  47.63  | EUR/MWh | HeatRoadMap    |
| 2050ZNES   | uranium   |   1.692 | EUR/MWh | Own Assumption |
| 2050ZNES   | waste     |  30     | EUR/MWh | Own Assumption |



## Technical parameters

|   year | parameter    | carrier   | tech     |      value | unit      | source                    |
|-------:|:-------------|:----------|:---------|-----------:|:----------|:--------------------------|
|   2030 | efficiency   | biomass   | st       |    0.35    | per unit  | DIW                       |
|   2030 | efficiency   | coal      | st       |    0.4     | per unit  | TYNDP2018                 |
|   2030 | efficiency   | gas       | ccgt     |    0.5     | per unit  | TYNDP2018                 |
|   2030 | efficiency   | gas       | ocgt     |    0.38    | per unit  | TYNDP2018                 |
|   2030 | efficiency   | hydro     | phs      |    0.75    | per unit  | roundtrip; DIW            |
|   2030 | efficiency   | hydro     | ror      |    0.9     | per unit  | DIW                       |
|   2030 | efficiency   | hydro     | rsv      |    0.9     | per unit  | DIW                       |
|   2030 | efficiency   | lignite   | st       |    0.4     | per unit  | TYNDP2018                 |
|   2030 | efficiency   | oil       | ocgt     |    0.35    | per unit  | TYNDP2018                 |
|   2030 | efficiency   | uranium   | st       |    0.33    | per unit  | TYNDP2018                 |
|   2030 | efficiency   | waste     | st       |    0.26    | per unit  | Own assumption            |
|   2030 | efficiency   | mixed     | st       |    0.26    | per unit  | Own assumption            |
|   2030 | efficiency   | lithium   | battery  |    0.85    | per unit  | roundtrip;Own assumption  |
|   2030 | efficiency   | cavern    | acaes    |    0.7     | per unit  | roundtrip;ZNES            |
|   2030 | efficiency   | hydrogen  | storage  |    0.4     | per unit  | roundtrip;ZNES            |
|   2030 | max_hours    | lithium   | battery  |    6.5     | h         | Plessmann                 |
|   2030 | max_hours    | hydro     | phs      |    8       | h         | Plessmann                 |
|   2030 | max_hours    | porous    | acaes    |  300       | h         | Own assumption            |
|   2030 | max_hours    | cavern    | acaes    |    3       | h         | ZNES                      |
|   2030 | max_hours    | hydrogen  | storage  |  168       | h         | eGo                       |
|   2030 | capex        | wind      | onshore  | 1182       | Euro/kW   | DIW                       |
|   2030 | capex        | wind      | offshore | 2506       | Euro/kW   | DIW                       |
|   2030 | capex        | solar     | pv       |  600       | Euro/kW   | DIW                       |
|   2030 | capex        | gas       | ocgt     |  400       | Euro/kW   | DIW                       |
|   2030 | capex        | gas       | ccgt     |  800       | Euro/kW   | DIW                       |
|   2030 | capex        | lithium   | battery  |  785       | Euro/kW   | IWES                      |
|   2040 | efficiency   | biomass   | st       |    0.4185  | per unit  | Own assumption            |
|   2040 | efficiency   | coal      | st       |    0.425   | per unit  | Own assumption            |
|   2040 | efficiency   | gas       | ccgt     |    0.53475 | per unit  | Own assumption            |
|   2040 | efficiency   | gas       | ocgt     |    0.373   | per unit  | Own assumption            |
|   2040 | efficiency   | hydro     | phs      |    0.75    | per unit  | roundtrip; DIW            |
|   2040 | efficiency   | hydro     | ror      |    0.9     | per unit  | DIW                       |
|   2040 | efficiency   | hydro     | rsv      |    0.9     | per unit  | DIW                       |
|   2040 | efficiency   | lignite   | st       |    0.4     | per unit  | Own assumption            |
|   2040 | efficiency   | oil       | ocgt     |    0.373   | per unit  | Own assumption            |
|   2040 | efficiency   | uranium   | st       |    0.335   | per unit  | Own assumption            |
|   2040 | efficiency   | waste     | st       |    0.26    | per unit  | Own assumption            |
|   2040 | efficiency   | mixed     | st       |    0.28    | per unit  | Own assumption            |
|   2040 | efficiency   | lithium   | battery  |    0.885   | per unit  | Own assumption            |
|   2040 | efficiency   | porous    | acaes    |    0.57    | per unit  | roundtrip; Own assumption |
|   2040 | efficiency   | cavern    | acaes    |    0.7     | per unit  | roundtrip; ZNES           |
|   2040 | max_hours    | lithium   | battery  |    6.5     | h         | Plessmann                 |
|   2040 | max_hours    | hydro     | phs      |    8       | h         | Plessmann                 |
|   2040 | max_hours    | porous    | acaes    |  300       | h         | Own assumption            |
|   2040 | max_hours    | cavern    | acaes    |    3       | h         | ZNES                      |
|   2050 | efficiency   | biomass   | st       |    0.487   | per unit  | DIW                       |
|   2050 | efficiency   | coal      | st       |    0.45    | per unit  | DIW                       |
|   2050 | efficiency   | gas       | ccgt     |    0.5695  | per unit  | Avg; DIW                  |
|   2050 | efficiency   | gas       | ocgt     |    0.366   | per unit  | Avg; DIW                  |
|   2050 | efficiency   | hydro     | phs      |    0.75    | per unit  | roundtrip; DIW            |
|   2050 | efficiency   | hydro     | ror      |    0.9     | per unit  | DIW                       |
|   2050 | efficiency   | hydro     | rsv      |    0.9     | per unit  | DIW                       |
|   2050 | efficiency   | lignite   | st       |    0.4     | per unit  | Avg; DIW                  |
|   2050 | efficiency   | oil       | ocgt     |    0.396   | per unit  | DIW                       |
|   2050 | efficiency   | uranium   | st       |    0.34    | per unit  | DIW                       |
|   2050 | efficiency   | waste     | st       |    0.26    | per unit  | Own assumption            |
|   2050 | efficiency   | mixed     | st       |    0.3     | per unit  | Own assumption            |
|   2050 | efficiency   | lithium   | battery  |    0.92    | per unit  | roundtrip; IWES           |
|   2050 | efficiency   | porous    | acaes    |    0.57    | per unit  | roundtrip; Own assumption |
|   2050 | max_hours    | lithium   | battery  |    6.5     | h         | Plessmann, p. 90          |
|   2050 | max_hours    | hydro     | phs      |    8       | h         | Plessmann, p. 90          |
|   2050 | max_hours    | porous    | acaes    |  300       | h         | Own assumption            |
|   2050 | avf          | wind      | onshore  |    1       | per unit  | Own assumption            |
|   2050 | avf          | wind      | offshore |    1       | per unit  | Own assumption            |
|   2050 | avf          | solar     | pv       |    1       | per unit  | Own assumption            |
|   2050 | avf          | biomass   | st       |    0.9     | per unit  | Own assumption            |
|   2050 | avf          | coal      | st       |    0.85    | per unit  | PRIMES                    |
|   2050 | avf          | gas       | ccgt     |    0.85    | per unit  | PRIMES                    |
|   2050 | avf          | gas       | ocgt     |    0.96    | per unit  | PRIMES                    |
|   2050 | avf          | hydro     | phs      |    1       | per unit  | Own assumption            |
|   2050 | avf          | hydro     | ror      |    1       | per unit  | Own assumption            |
|   2050 | avf          | hydro     | rsv      |    1       | per unit  | Own assumption            |
|   2050 | avf          | lignite   | st       |    0.85    | per unit  | PRIMES                    |
|   2050 | avf          | oil       | ocgt     |    0.9     | per unit  | PRIMES                    |
|   2050 | avf          | mixed     | st       |    0.9     | per unit  | Own assumption            |
|   2050 | avf          | uranium   | st       |    0.9     | per unit  | Own assumption            |
|   2050 | avf          | waste     | st       |    0.9     | per unit  | Own assumption            |
|   2050 | avf          | lithium   | battery  |    1       | per unit  | Own assumption            |
|   2050 | avf          | porous    | acaes    |    1       | per unit  | Own assumption            |
|   2050 | vom          | wind      | onshore  |    0       | Euro/Mwh  | Plessmann                 |
|   2050 | vom          | wind      | offshore |    0       | Euro/Mwh  | Plessmann                 |
|   2050 | vom          | solar     | pv       |    0       | Euro/Mwh  | Plessmann                 |
|   2050 | vom          | biomass   | st       |   10       | Euro/Mwh  | Own assumption            |
|   2050 | vom          | coal      | st       |    6       | Euro/Mwh  | DIW, p. 78                |
|   2050 | vom          | gas       | ccgt     |    4       | Euro/Mwh  | DIW, p. 78                |
|   2050 | vom          | gas       | ocgt     |    3       | Euro/Mwh  | DIW, p. 78                |
|   2050 | vom          | hydro     | phs      |    0       | Euro/Mwh  | DIW, p. 78                |
|   2050 | vom          | hydro     | ror      |    0       | Euro/Mwh  | DIW, p. 78                |
|   2050 | vom          | hydro     | rsv      |    0       | Euro/Mwh  | DIW, p. 78                |
|   2050 | vom          | lignite   | st       |    7       | Euro/Mwh  | DIW, p. 78                |
|   2050 | vom          | uranium   | st       |    8.5     | Euro/Mwh  | DIW, p. 78, AVG           |
|   2050 | vom          | oil       | ocgt     |    3       | Euro/Mwh  | DIW, p. 78                |
|   2050 | vom          | mixed     | st       |    5       | Euro/Mwh  | Own assumption            |
|   2050 | vom          | waste     | st       |   10       | Euro/Mwh  | Own assumption            |
|   2050 | vom          | lithium   | battery  |    0       | Euro/Mwh  | Plessmann, p. 90          |
|   2050 | fom          | wind      | onshore  |   35       | Euro/kWa  | DIW, p.78                 |
|   2050 | fom          | wind      | offshore |   80       | Euro/kWa  | DIW, p.78                 |
|   2050 | fom          | solar     | pv       |   25       | Euro/kWa  | DIW, p.78                 |
|   2050 | fom          | biomass   | st       |  100       | Euro/kWa  | DIW, p.78                 |
|   2050 | fom          | coal      | st       |   25       | Euro/kWa  | DIW, p.78                 |
|   2050 | fom          | gas       | ccgt     |   20       | Euro/kWa  | DIW, p.78                 |
|   2050 | fom          | gas       | ocgt     |   15       | Euro/kWa  | DIW, p.78                 |
|   2050 | fom          | hydro     | phs      |   20       | Euro/kWa  | DIW, p.78                 |
|   2050 | fom          | hydro     | ror      |   60       | Euro/kWa  | DIW, p.78                 |
|   2050 | fom          | hydro     | rsv      |   20       | Euro/kWa  | DIW, p.78                 |
|   2050 | fom          | lignite   | st       |   30       | Euro/kWa  | DIW, p.78                 |
|   2050 | fom          | oil       | ocgt     |    6       | Euro/kWa  | DIW, p.78                 |
|   2050 | fom          | lithium   | battery  |   10       | Euro/kWha | Schill2018                |
|   2050 | capex        | wind      | onshore  | 1075       | Euro/kW   | DIW, p. 75                |
|   2050 | capex        | wind      | offshore | 2093       | Euro/kW   | DIW, p. 75                |
|   2050 | capex        | solar     | pv       |  425       | Euro/kW   | DIW, p. 75                |
|   2050 | capex        | biomass   | st       | 1951       | Euro/kW   | DIW, p. 75                |
|   2050 | capex        | coal      | st       | 1300       | Euro/kW   | DIW, p. 75                |
|   2050 | capex        | gas       | ccgt     |  800       | Euro/kW   | DIW, p. 75                |
|   2050 | capex        | gas       | ocgt     |  400       | Euro/kW   | DIW, p. 75                |
|   2050 | capex        | hydro     | phs      | 2000       | Euro/kW   | DIW, p. 75                |
|   2050 | capex        | hydro     | ror      | 3000       | Euro/kW   | DIW, p. 75                |
|   2050 | capex        | hydro     | rsv      | 2000       | Euro/kW   | DIW, p. 75                |
|   2050 | capex        | lignite   | st       | 1500       | Euro/kW   | DIW, p. 75                |
|   2050 | capex        | oil       | ocgt     |  400       | Euro/kW   | DIW, p. 75                |
|   2050 | capex_energy | lithium   | battery  |  187       | Euro/kWh  | Schill2018                |
|   2050 | capex_power  | lithium   | battery  |   35       | Euro/kWh  | Schill2018                |
|   2050 | lifetime     | wind      | onshore  |   25       | a         | DIW, p. 72                |
|   2050 | lifetime     | wind      | offshore |   25       | a         | DIW, p. 72                |
|   2050 | lifetime     | solar     | pv       |   25       | a         | DIW, p. 72                |
|   2050 | lifetime     | biomass   | st       |   30       | a         | DIW, p. 72                |
|   2050 | lifetime     | coal      | st       |   40       | a         | DIW, p. 72                |
|   2050 | lifetime     | gas       | ccgt     |   30       | a         | DIW, p. 72                |
|   2050 | lifetime     | gas       | ocgt     |   30       | a         | DIW, p. 72                |
|   2050 | lifetime     | hydro     | phs      |   50       | a         | DIW, p. 72                |
|   2050 | lifetime     | hydro     | ror      |   50       | a         | DIW, p. 72                |
|   2050 | lifetime     | hydro     | rsv      |   50       | a         | DIW, p. 72                |
|   2050 | lifetime     | lignite   | st       |   40       | a         | DIW, p. 72                |
|   2050 | lifetime     | oil       | ocgt     |   40       | a         | DIW, p. 72                |
|   2050 | lifetime     | lithium   | battery  |   10       | a         | Plessmann, p. 90          |
|   2050 | efficiency   | redox     | battery  |    0.75    | per unit  | roundtrip;ZNES            |
|   2050 | efficiency   | hydrogen  | storage  |    0.4     | per unit  | roundtrip;ZNES            |
|   2050 | efficiency   | cavern    | acaes    |    0.7     | per unit  | roundtrip;ZNES            |
|   2050 | max_hours    | redox     | battery  |    3.3     | h         | ZNES                      |
|   2050 | max_hours    | hydrogen  | storage  |  168       | h         | eGo                       |
|   2050 | max_hours    | cavern    | acaes    |    3       | h         | ZNES                      |
|   2050 | lifetime     | redox     | battery  |   25       | a         | Schill2018                |
|   2050 | lifetime     | hydrogen  | storage  |   22.5     | a         | Schill2018                |
|   2050 | lifetime     | cavern    | acaes    |   30       | a         | Schill2018                |
|   2050 | capex_energy | redox     | battery  |   70       | Euro/kWh  | Schill2018                |
|   2050 | capex_energy | hydrogen  | storage  |    0.2     | Euro/kWh  | Schill2018                |
|   2050 | capex_energy | cavern    | acaes    |   40       | Euro/kWh  | Schill2018                |
|   2050 | capex_power  | redox     | battery  |  600       | Euro/kW   | Schill2018                |
|   2050 | capex_power  | hydrogen  | storage  | 1000       | Euro/kW   | Schill2018                |
|   2050 | capex_power  | cavern    | acaes    |  750       | Euro/kW   | Schill2018                |
|   2050 | fom          | redox     | battery  |   10       | Euro/kWha | Schill2018                |
|   2050 | fom          | hydrogen  | storage  |   10       | Euro/kWha | Schill2018                |
|   2050 | fom          | cavern    | acaes    |   10       | Euro/kWha | Schill2018                |
|   2050 | vom          | redox     | battery  |    1       | Euro/Mwh  | Schill2018                |
|   2050 | vom          | hydrogen  | storage  |    1       | Euro/Mwh  | Schill2018                |
|   2050 | vom          | cavern    | acaes    |    1       | Euro/Mwh  | Schill2018                |

## Installed capacities

The table show the installed capacities for path towards 100% renewable energy supply
fomr 2030 to 2050.

| scenario   | name             | AT   | BE   | CH   | CZ   | DE    | DK   | FR    | LU   | NL   | NO   | PL   | SE   |
|:-----------|:-----------------|:-----|:-----|:-----|:-----|:------|:-----|:------|:-----|:-----|:-----|:-----|:-----|
| 2030NEPC   | biomass-st       | 0.6  | 1.3  | 1.3  | 1.2  | 6.0   | 1.9  | 3.6   | 0.1  | 0.5  | 0.1  | 1.8  | 4.5  |
| 2030NEPC   | oil-ocgt         | 0.2  | -    | -    | -    | 0.9   | 0.8  | 1.5   | -    | -    | -    | -    | -    |
| 2030NEPC   | solar-pv         | 4.5  | 5.1  | 5.6  | 3.5  | 104.5 | 2.9  | 31.5  | 0.2  | 11.4 | 0.4  | 2.4  | 1.7  |
| 2030NEPC   | mixed-st         | 1.0  | 1.2  | 1.0  | 1.5  | 4.1   | 0.1  | -     | 0.1  | 3.5  | -    | 7.3  | 0.4  |
| 2030NEPC   | lithium-battery  | -    | -    | -    | -    | 12.5  | -    | -     | -    | -    | -    | -    | -    |
| 2030NEPC   | lignite-st       | -    | -    | -    | 4.8  | 9.0   | -    | -     | -    | -    | -    | 7.4  | -    |
| 2030NEPC   | hydrogen-storage | -    | -    | -    | -    | 3.0   | -    | -     | -    | -    | -    | -    | -    |
| 2030NEPC   | uranium-st       | -    | -    | 1.2  | 4.1  | -     | -    | 37.6  | -    | 0.5  | -    | 3.0  | 6.9  |
| 2030NEPC   | hydro-phs        | 6.1  | 1.2  | 4.6  | 1.0  | 9.8   | -    | 5.5   | 1.0  | -    | 1.1  | 1.5  | -    |
| 2030NEPC   | gas-ocgt         | 1.4  | 2.2  | -    | 0.5  | 10.0  | 0.1  | 3.9   | -    | 2.6  | 0.1  | 2.0  | -    |
| 2030NEPC   | other-res        | -    | -    | -    | -    | 1.3   | -    | -     | -    | -    | -    | -    | -    |
| 2030NEPC   | gas-ccgt         | 2.7  | 4.2  | -    | 0.9  | 23.4  | 0.3  | 7.6   | -    | 5.0  | 0.3  | 3.8  | -    |
| 2030NEPC   | wind-onshore     | 5.0  | 3.3  | 0.4  | 1.0  | 85.5  | 5.6  | 36.3  | 0.2  | 6.7  | 3.3  | 9.2  | 10.8 |
| 2030NEPC   | cavern-acaes     | -    | -    | -    | -    | 1.0   | -    | -     | -    | -    | -    | -    | -    |
| 2030NEPC   | coal-st          | -    | -    | -    | 0.3  | 8.1   | 0.4  | -     | -    | 4.6  | -    | 13.8 | 0.1  |
| 2030NEPC   | wind-offshore    | -    | 2.3  | -    | -    | 17.0  | 2.9  | 7.0   | -    | 11.5 | -    | 2.2  | 0.2  |
| 2040GCA    | gas-ccgt         | 2.0  | 3.3  | -    | 0.7  | 20.1  | -    | 5.9   | -    | 5.0  | -    | 1.8  | -    |
| 2040GCA    | oil-ocgt         | 0.2  | -    | -    | 0.2  | 0.2   | 0.3  | 1.0   | -    | -    | -    | 3.9  | -    |
| 2040GCA    | biomass-st       | 0.6  | 1.3  | 1.3  | 1.2  | 6.6   | 1.9  | 3.6   | 0.1  | 0.5  | 0.1  | 1.8  | 4.3  |
| 2040GCA    | mixed-st         | 1.0  | 1.7  | 1.0  | 1.5  | 10.3  | 0.1  | -     | 0.1  | 3.5  | -    | 7.3  | 0.4  |
| 2040GCA    | solar-pv         | 5.6  | 22.0 | 12.6 | 5.2  | 141.0 | 7.5  | 60.0  | 1.1  | 46.0 | 3.0  | 42.5 | 6.7  |
| 2040GCA    | lignite-st       | -    | -    | -    | 1.3  | -     | -    | -     | -    | -    | -    | 1.9  | -    |
| 2040GCA    | coal-st          | -    | -    | -    | 0.3  | 8.3   | -    | -     | -    | 3.4  | -    | 8.3  | -    |
| 2040GCA    | wind-offshore    | -    | 8.3  | -    | -    | 33.8  | 7.8  | 20.0  | -    | 23.4 | 0.4  | 7.0  | 1.3  |
| 2040GCA    | uranium-st       | -    | -    | -    | 3.3  | -     | -    | 37.6  | -    | -    | -    | 7.5  | 3.7  |
| 2040GCA    | gas-ocgt         | 1.0  | 1.7  | -    | 0.3  | 10.4  | -    | 3.0   | -    | 2.6  | -    | 0.9  | -    |
| 2040GCA    | wind-onshore     | 5.5  | 7.7  | 2.6  | 1.3  | 81.6  | 7.2  | 49.0  | 0.2  | 7.4  | 10.0 | 32.9 | 17.4 |
| 2040GCA    | hydro-phs        | 6.1  | 1.9  | 6.7  | 1.1  | 10.2  | -    | 5.5   | 1.0  | 2.5  | 1.1  | 2.3  | -    |
| 2050ANGUS  | wind-offshore    | -    | 3.0  | -    | -    | 33.8  | 25.6 | -     | -    | 15.9 | 3.0  | -    | 3.0  |
| 2050ANGUS  | solar-pv         | 12.1 | 24.1 | 15.0 | 13.0 | 150.0 | 2.0  | 103.1 | 1.0  | 22.2 | 5.4  | 24.2 | 8.9  |
| 2050ANGUS  | redox-battery    | -    | -    | -    | -    | 0.9   | 0.1  | 0.1   | -    | -    | -    | -    | -    |
| 2050ANGUS  | lignite-st       | -    | -    | -    | -    | -     | -    | -     | -    | -    | -    | -    | -    |
| 2050ANGUS  | oil-ocgt         | -    | -    | -    | -    | -     | -    | -     | -    | -    | -    | -    | -    |
| 2050ANGUS  | mixed-st         | -    | -    | -    | -    | -     | -    | -     | -    | -    | -    | -    | -    |
| 2050ANGUS  | lithium-battery  | 0.2  | 0.3  | 0.3  | 2.5  | 15.6  | 0.9  | 3.4   | 0.1  | 1.3  | -    | 4.5  | 3.2  |
| 2050ANGUS  | hydrogen-storage | -    | 1.8  | -    | 0.2  | 10.1  | 5.0  | 26.0  | 0.6  | 7.6  | -    | 0.3  | -    |
| 2050ANGUS  | hydro-phs        | 10.7 | 2.3  | 5.4  | 1.8  | 12.8  | -    | 13.4  | 1.7  | -    | 17.3 | 3.8  | -    |
| 2050ANGUS  | gas-ocgt         | 0.5  | 0.8  | 0.7  | 0.6  | 4.4   | 0.3  | 5.4   | 0.1  | 1.0  | -    | 1.0  | -    |
| 2050ANGUS  | gas-ccgt         | 1.0  | 1.6  | 1.3  | 1.2  | 8.6   | 0.7  | 10.6  | 0.2  | 2.0  | -    | 2.0  | -    |
| 2050ANGUS  | coal-st          | -    | -    | -    | -    | -     | -    | -     | -    | -    | -    | -    | -    |
| 2050ANGUS  | cavern-acaes     | -    | 0.4  | -    | 0.9  | 3.4   | 0.2  | 0.2   | 0.1  | 1.7  | -    | 1.7  | -    |
| 2050ANGUS  | biomass-st       | 3.5  | 4.8  | 1.2  | 5.0  | 27.8  | 3.8  | 28.2  | -    | 4.0  | 0.5  | 14.2 | 5.5  |
| 2050ANGUS  | other-res        | -    | -    | -    | -    | 1.2   | -    | -     | -    | -    | -    | -    | -    |
| 2050ANGUS  | wind-onshore     | 6.9  | 10.9 | 1.4  | 10.2 | 98.3  | 18.7 | 124.2 | 0.7  | 15.0 | 12.2 | 81.9 | 24.2 |




## Grid

![Installed transmission capacities in 2030](grid-scenarioANGUS2030.pdf){width=60%}

![Installed transmission capacities in 2040](grid-scenarioANGUS2040.pdf){width=60%}

![Installed transmission capacities in 2050](grid-scenarioANGUS2050.pdf){width=60%}

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
