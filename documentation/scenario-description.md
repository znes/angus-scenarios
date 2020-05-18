---
title: ANGUS II Scenario Description
author: Simon Hilpert and Clemens Wingenbach
date: January, 2020
header: This is fancy
footer: So is this
geometry: "left=2cm, right=2cm, top=2cm, bottom=2cm"
bibliography: angus-literature.bib
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
energy supply in Germany by 2050. The developed scenarios are based on the TYNDP2018,
the NEP2019, the
e-Highway 100%-RES scenario and the UBA RESCUE scenarios. Their main purpose
is to generate storage operation profiles (power, energy) to assess underground storage
technologies with regard to techno-ecnomic indicators. Therefore, the
shadow prices of the developed techno-economic energy system model play an
important role as an economic signal for the storage dispatch and the model coupling
(see ANGUS Case Studies). Hence, high priority is given to sensitivities that have a
major effect on the storage dispatch and requirements of the future German
energy system.

## Existing Scenarios

The scientific foundation for the ANGUS scenarios is provided by an alignment wit
prominent scenarios from literature. For the mid-term perspective, the
*Netzentwicklungsplan (NEP)* in combination with the
Ten Year Netwok Development Plan (TYNDP) are considered. In addition, the e-Highway2050
scenarios are used as a starting point for the long-term (2050) system.

The NEP is developed by the German transmission system
operator (TSOs) to plan the transmission grid in Germany. It is based on a broad
public consultation phase to enable high acceptance of planned grid expansion.
Similarly, TYNDP is developed by the European TSOs with regard to the European grid.
The processes of the national NEP and the TYNDP are coordinated to ensure coherent national
and international planning. Both of these scenarios are updated every two years.
Hence, the projects reflect current and expected socio-economic developments
as well as recent relevant policy decisions.  Due to the public consultation and
their prominent nature, these scenarios constitute import visions for the future
European energy system. Another important project in the Eurpean context are the
EUCO scenarios. Their data has been used as input data for the
TNYDP2018. Thus, in the ANGUS project the focus will be given to the TNYDP2018
scenarios for modelling the electrical neigbouring countries of Germany in the mid-term
future.

The NEP as well as the TYNDP are focussing on the short to mid-term perspective. Hence,
within the ANGUS project another prominent scenario development project,
the e-Highway2050 project, is used as a foundation for the scenario frame.
The project has been funded by the European Commission and aimed to develop a
plan for the European transmission network from 2020
to 2050. One important part of this study is the support of EU’s overall policy
objectives with regard to energy. The study builds upon the TYNDP2016 and
includes scenarios for 100% renewable energy supply in 2050.

The scenarios projects have been chose as the major guideline for the ANGUS project.
However other additional national scenarios are considered with respect to the scenario
development. These include the BMWI Langfristszenarien for Germany developed by
the Fraunhofer ISI and the UBA RESUCE [@katja_purr_wege_2019] scenarios.

### System with high shares of RE
In literature different scenarios for up to 100% renewable energy systems can
found. Figure \ref{scenario-comparison} shows installed capacities of renewable energies
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
renewable energy source. The role of biomass for 100% long-term scenarios has been
discussed for example by [@szarka_interpreting_2017].

![Installed renewable capacities in scenarios from literature.\label{scenario-comparison}](figures/scenario-comparison.pdf)

The lowest capacities are found in the BMWI Reference scenario. However, capacity
factors
for wind in the scenario are significantly higher compared to the other scenarios.
In addition, this scenario only comes with a share of approx. 82% RE.
The highest capacities of wind and pv are obtained in the RESCUE GL scenario. Here
the 100% RE, no import and the higher demand of 796 TWh are the driving factors.
Within the set of scenarios, the wind and pv capacities of e-Highway scenario are
rather located at the lower end of the range. The main reason is the high biomass
potential, increasing hydro capacities (in particular in Norway) and higher
offshore wind capacities. This results in significant imports in Germany, but also lower
in installed capacities of onshore wind and pv. In addtion to the before mentioned
factors, system flexibility is another important determinate. Here grid
infrastructure (spatial flexibility) and storages (temporal flexbiliy) have to
be considered.

# Mathematical Model

Subsequently a mathematical description of the linear programming
least cost optimisation model is given. Total operational cost of the system are
minimised with subject to system constraints. The equations for the
mathematical model are provided for the different types of the
oemof-tabular components. Subsequently, endogenous model variables are
denoted with $x$, while exogenous parameters are denoted with $c$. The full set
of equations for oemof-tabular components can be found in the online documentation
of the software.



## Component overview

The table shows the carrier and technologies present in the scenarios and their
corresponding type (i.e. oemof tabular class) and set.

| carrier     | tech      | type         | set name   | index   |
|:------------|:----------|:-------------|:-----------|:--------|
| wind        | onshore   | volatile     | V          | v       |
| wind        | offshore  | volatile     | V          | v       |
| other       | res       | dispatchable | D          | d       |
| hydro       | ror       | volatile     | V          | v       |
| biomass     | st        | conversion   | C          | c       |
| solar       | pv        | volatile     | V          | v       |
| gas         | ccgt      | dispatchable | D          | d       |
| gas         | ocgt      | dispatchable | D          | d       |
| coal        | st        | dispatchable | D          | d       |
| lignite     | st        | dispatchable | D          | d       |
| uranium     | st        | dispatchable | D          | d       |
| oil         | ocgt      | dispatchable | D          | d       |
| mixed       | st        | dispatchable | D          | d       |
| waste       | st        | dispatchable | D          | d       |
| lithium     | battery   | storage      | S          | s       |
| hydrogen    | storage   | storage      | S          | s       |
| redox       | battery   | storage      | S          | s       |
| cavern      | acaes     | storage      | S          | s       |
| hydro       | phs       | storage      | S          | s       |
| hydro       | reservoir | reservoir    | R          | r       |
| electricity | load      | load         | L          | l       |
| electricity | line      | link         | n          | N       |



\newpage
# ANGUS Scenario Assumptions

## Spatial and temporal resolution

The scenarios model the Western European energy system with one
node per country. Countries modelled are:

**AT, BE, CH, CZ, DE, DK, FR, IT, LU, NL, NO, PL, SE.**

The model simulates the system on an hourly basis for one year using a
perfect foresight approach with the years 2030 and 2050.  Due to the regional
focus of this study the German energy system is modelled with greater detail
compared to  the neigbouring countries.

**Implications & Limitations**: Intra-country grid constraints are not
reflected by the model. Hence, renewable energy curtailment and/or storage
demand may be underestimated.

## Grid

The grid for 2030 and 2040 is based on the TYNDP2018 (see Annex), while the grid for
2050 is based on the e-Highway 100% RES scenario. Figure \ref{grid_2050} shows
the installed transmission capacities of the 2050 electricity system. The transmission
system is modelled with a transshipment approach assuming a loss of 0.03 on the lines.

![Installed transmission capacities in 2050.\label{grid_2050}](figures/grid-scenario2050REF.pdf){width=50%}

## Demand

### Conventional electricity demand
The German goals regarding efficiency aim to reduce the electricity demand
by 10% until 2020 and 25% by 2050 compared to 2008 levels (403.8 TWh).
The development of future electricity demand strongly depends on demographic and
economic development as well as implemented efficiency measures.
In literature, different values can be found. Assumptions regarding the
electricity demand are an important driving factor for the energy system.
At the same time, these values come with a high degree of uncertainty
(Result of the ANGUS Scenario Workshop). While for example the conventional
electricity demand within the *Reference Scenario* of the German *BMWI Langfristszenarien*
accounts for 441.2 TWh in 2030 and 417.2 TWh in 2050 respectively, the demand in the NEP2019
scenarios for 2030 is slightly higher (477 TWh). Hence, depending on assumptions
(demographics, efficiency and rebound effects, economic activity) the amount of
conventional electricity applications can vary.

### Sector coupling
Despite a decreasing demand due to efficiency measures, the electrification
of other sectors (heat, transport) will create an additional demand for electricity.
Currently the heat demand for residential heating accounts for 122.4 TWh hot water
and 678.5 TWh space heating (2017). The German government set a goal of 60-80%
reduction for this sector 2050. These values are very ambitious, as current
values of insulation are lacking behind necessary rates. Heat demand for hot water and
space heating in the RESCUE scenarios ranges from 436.8 TWh (green late scenario: GL) to 246.2 TWh
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
(assuming an coefficienct of performance of approximately 3). For the 2030NEPC a
heat demand covered by heat pumps of 87 TWh is assumed.  


The electricity demand (excluding electricity for decentral heat pumps)
for the different scenarios is given in the Table below.

|    |   2030DG |   2030NEPC |   2040DG |   2040GCA |   2050REF |
|:---|---------:|-----------:|---------:|----------:|----------:|
| AT |    80.7  |      76.55 |    91.34 |     80.5  |     84.82 |
| BE |    88.71 |      88.78 |    92.27 |     91.52 |    121.25 |
| CH |    58.07 |      58.28 |    62.98 |     57.93 |     77.33 |
| CZ |    75.87 |      70.86 |    86.57 |     76.43 |     71.76 |
| DE |   571    |     547    |   601    |    601    |    613    |
| DK |    50.21 |      46.96 |    57.88 |     53.78 |     42.67 |
| FR |   474.66 |     466.74 |   493.5  |    468.62 |    649.45 |
| LU |    11.07 |      11.05 |    11.59 |      8.26 |      7.38 |
| NL |   129.79 |     118.53 |   147.85 |    136.61 |    160.72 |
| NO |   150.66 |     149.93 |   153.63 |    148.09 |    102.02 |
| PL |   219.3  |     206.68 |   234.79 |    251.3  |    172.22 |
| SE |   140.38 |     143.04 |   137.34 |    145.84 |    131.56 |


The heat demand covered by heat pumps for each scenario is given in the Table
below.

| Scenario   |   Amount in TWh |
|:-----------|---------:|
| 2050REF    |      284 |
| 2040DG     |      195 |
| 2030DG     |       57 |
| 2030NEPC   |       87 |
| 2040GCA    |      195 |


Demand profiles are calculated from the OPSD dataset of the ENTSOE
timeseries for the selected weather year (2011).

**Implications & Limitations**:

* Due to the historic demand profiles, future
flexibilities like smart operation of certain applications and industry
processes are not modelled.
* The model only covers the residential hot water and space heating demand.
* Electric vehicles are modelled without specific profile for charging / discharging but only
with a constant additional base load.


## Generation capacity

The different scenarios are based on the NEP2019, TYNDP2018 and the e-Highway
project.

* NEP2030C: Installed capacities in Germany are based on the NEP2019 scenario 2030C. The
capacities of neighbouring countries are based on the TYNDP2018-2030ST vision. The
renewable share of produced energy in Germany in this scenario is approx. 68 %.
* 2040GCA: This scenario is based on the TYNDP2018-GCA vision. Similary
the *DG* scenarios are  based on the TYNDP2018-DG scenario.
* 2050REF: The base for this scenario is the e-Highway 100 % RES scenario. It scenario
strongly depends on hydro capacity expansion in Norway. The  biomass potential
has been reduced and the PV and wind capacities have been increased to
match with the demand values of the RESCUE GL scenario.

The installed capacities in Germany are shown in the Figure \ref{installed_capacities}
below.

![Installed generation capacity in Germany from 2030 to 2050 with different shares of renewables in 2050.\label{installed_capacities}](figures/DE-installed_capacities.pdf){width=100%}


## Storage Capacities

PHS storage capacity has been fixed to values from the TYNDP2018 and the e-Highway2050
scenario. For the short-term (lithium) and long-term (hydrogen) storages
the results are shown in the table below in GW installed capacity. It can
be seen that only for the 100% scenario in 2050 long-term storage is required.
For 2030 no additional storage is invested. Note, that the storage demand
due to grid constraints not modelled inside the countries might be higher.


|          |   2030DG |   2030NEPC |   2040DG |   2040GCA |   2050REF |
|:---------|---------:|-----------:|---------:|----------:|----------:|
| Lithium (GW) |        0 |          0 |  3225.55 |    4528.6 |   6075.72 |
| Hydrogen (GW) |        0 |          0 |     0    |       0   |   5089.42 |


## Renewable Energies


### Wind and PV
Onshore wind and pv timeseries are based on renewables ninja for each country.
The offshore profiles are taken from the Vernetzen-project and adapted with a
correction factor of 0.8 which has been derived from the energy production in
the e-Highway scenarios.


| country   |   offshore |   onshore |   pv |   ror |
|:----------|-----------:|----------:|-----:|------:|
| AT        |        - |      1507 | 1291 |  3058 |
| BE        |       3939 |      2406 | 1135 |  1335 |
| CH        |        - |      1354 | 1416 |  3832 |
| CZ        |        - |      1875 | 1226 |  1974 |
| DE        |       3976 |      1951 | 1151 |  4043 |
| DK        |       4224 |      2670 |  977 |     - |
| FR        |       3295 |      2040 | 1265 |  2722 |
| LU        |        - |      2917 | 1192 |  2644 |
| NL        |       4025 |      1921 | 1095 |  1518 |
| NO        |       4341 |      3562 |  811 |  2028 |
| PL        |       3964 |      1834 | 1113 |  1493 |
| SE        |       3792 |      2654 |  862 |  2161 |


### Biomass potential

The maximum biomass potential per country is derived from the hotmaps project [@hotmaps_hotmaps_2019]
and is equal for all scenarios in the ANGUS project. The potential does not cover
waste but only agriculture and forestry residues. The potential for Germany has
been reduced to match with the
RESCUE scenarios. This limit does only apply for the year 2050. For previous years
no limit on biomass potential is given. With an efficiency of 0.487
for biomass to electricity conversion the potential in Germany is approx.
21.9 TWh{_el}.

Biomass potential:

|    | Amount in TWh |
|:---|-----------:|
| AT |  23.6111   |
| BE |   8.08333  |
| CH |   0        |
| CZ |  32.7778   |
| DE |  150.167   |
| DK |  13.5556   |
| FR |  45    |
| LU |   0.611111 |
| NL |   2.80556  |
| NO |   0        |
| PL |  71.3611   |
| SE |  86.75     |


### Hydro
For 2030 and 2040 hydro data has been calculated based on the TYNDP2018. The reservoir
(rsv) capacity is calculated by subtracting the column *hydro-pump* from column *hydro turbine*
in the original data source. Therefore, it is assumed, that each pumped hydro storage
(phs) has equal pump/turbine capacities. For 2050 e-Highway database is used as a source.
The storage energy capacity (max-hours) for pumped hydro is based on [@geth_overview_2015].
For the rsv capacity the Restore2050 data is used where storage capacities are
provided in addition to the installed capacity.

The inflow in run of river and reservoirs is modelled
with the inflow timeseries of the Restore2050 project. The total hydro inflow from
the Restore2050 project is split by the ror-share for each scenario year. For Norway
and Sweden the reservoir inflow has been scaled up to match with the e-Highway results.
Similary, the run of river units for all countries except Sweden and Norway have been
scaled by a factor of 1.6. The resulting fullloadhours are show in the Table below.



\clearpage

# Annex

## Hydro data

| country   |   year |      phs |   phs-max-hours |        ror |   ror-share |      rsv |   rsv-factor |   rsv-max-hours |
|:----------|-------:|---------:|----------------:|-----------:|------------:|---------:|-------------:|----------------:|
| AT        |   2015 |  2971.1  |              33 |  5542.7    |   0.6515    |  2964.9  |    1         |             857 |
| AT        |   2030 |  6055.33 |              33 |  4671.9    |   0.493889  |  4787.52 |    1.61473   |             857 |
| AT        |   2040 |  6055.33 |              33 |  4671.9    |   0.493889  |  4787.52 |    1.61473   |             857 |
| AT        |   2050 | 10733    |              33 |  7401.16   |   0.565961  |  5676    |    1.9144    |             857 |
| BE        |   2015 |  1308    |               4 |   114.56   |   1         |     0    |    1         |             500 |
| BE        |   2030 |  1150    |               4 |   117      |   0.425455  |   158    |    1         |             500 |
| BE        |   2040 |  1908    |               4 |   117      |   0.425455  |   158    |    1         |             500 |
| BE        |   2050 |  2308    |               4 |   331.972  |   1         |     0    |    0         |             500 |
| CH        |   2015 |  3940    |             136 |   190      |   0.0381388 |  4791.8  |    1         |             906 |
| CH        |   2030 |  4593    |             136 |  4139      |   0.315328  |  8987    |    1.8755    |             906 |
| CH        |   2040 |  6722    |             136 |  4139      |   0.315328  |  8987    |    1.8755    |             906 |
| CH        |   2050 |  5443    |             136 |  4122.7    |   0.336473  |  8130    |    1.69665   |             906 |
| CZ        |   2015 |  1175    |               5 |   440      |   0.40367   |   650    |    1         |            1111 |
| CZ        |   2030 |  1000    |               5 |   365      |   0.879518  |    50    |    0.0769231 |            1111 |
| CZ        |   2040 |  1145    |               5 |   365      |   0.879518  |    50    |    0.0769231 |            1111 |
| CZ        |   2050 |  1787    |               5 |   454.846  |   0.357065  |   819    |    1.26      |            1111 |
| DE        |   2015 |  8699    |               6 |  3988.62   |   0.724332  |  1518    |    1         |             592 |
| DE        |   2030 |  9791.6  |               6 |  4329      |   0.812973  |   995.9  |    0.656061  |             592 |
| DE        |   2040 | 10244    |               6 |  4329      |   0.874722  |   620    |    0.408432  |             592 |
| DE        |   2050 | 12799    |               6 |  4233      |   0.872244  |   620    |    0.408432  |             592 |
| DK        |   2015 |     0    |               6 |     9      |   1         |     0    |    1         |                 |
| DK        |   2030 |     0    |               6 |     6.6082 |   1         |     0    |    0         |                 |
| DK        |   2040 |     0    |               6 |     6.6082 |   1         |     0    |    0         |                 |
| DK        |   2050 |     0    |               6 |    13.3102 |   1         |     0    |    0         |                 |
| FR        |   2015 |  4965    |              15 | 10314      |   0.556671  |  8214    |    1         |            1201 |
| FR        |   2030 |  5500    |              15 | 13797      |   0.627307  |  8197    |    0.99793   |            1201 |
| FR        |   2040 |  5500    |              15 | 13600      |   0.62963   |  8000    |    0.973947  |            1201 |
| FR        |   2050 | 13420    |              15 | 10318.6    |   0.36182   | 18200    |    2.21573   |            1201 |
| LU        |   2015 |     0    |               4 |    25      |   0.694444  |    11    |    1         |            2840 |
| LU        |   2030 |  1026    |               4 |    34      |   0.106918  |   284    |   25.8182    |            2840 |
| LU        |   2040 |  1026    |               4 |    34      |   0.106918  |   284    |   25.8182    |            2840 |
| LU        |   2050 |  1650.68 |               4 |   149.203  |   1         |     0    |    0         |            2840 |
| NL        |   2015 |     0    |               6 |    38      |   1         |     0    |    1         |                 |
| NL        |   2030 |     0    |               6 |    38      |   1         |     0    |    0         |                 |
| NL        |   2040 |  2500    |               6 |    38      |   1         |     0    |    0         |                 |
| NL        |   2050 |     0    |               6 |   104.435  |   1         |     0    |    0         |                 |
| NO        |   2015 |     0    |             314 |  1351.8    |   0.0478322 | 26909.5  |    1         |            3139 |
| NO        |   2030 |  1114.71 |             314 |     0      |   0         | 34702.2  |    1.28959   |            3139 |
| NO        |   2040 |  1114.71 |             314 |     0      |   0         | 34702.2  |    1.28959   |            3139 |
| NO        |   2050 | 17291    |             314 | 28141      |   0.398518  | 42473    |    1.57836   |            3139 |
| PL        |   2015 |  1770.12 |               5 |   377.84   |   0.707552  |   156.17 |    1         |            5477 |
| PL        |   2030 |  1488    |               5 |  1033      |   1         |     0    |    0         |            5477 |
| PL        |   2040 |  2292    |               5 |  1033      |   1         |     0    |    0         |            5477 |
| PL        |   2050 |  3790    |               5 |  2078.8    |   1         |     0    |    0         |            5477 |
| SE        |   2015 |     0    |             793 |     0      |   0         | 15956    |    1         |            3456 |
| SE        |   2030 |     0    |             793 |     0      |   0         | 16184    |    1.01429   |            3456 |
| SE        |   2040 |     0    |             793 |     0      |   0         | 16184    |    1.01429   |            3456 |
| SE        |   2050 |     0    |             793 | 10775.2    |   0.335066  | 21383.3  |    1.34014   |            3456 |


\newpage
## Carrier cost

| scenario   | carrier   | source         | unit    |   value |
|:-----------|:----------|:---------------|:--------|--------:|
| 2030DG     | biomass   | HeatRoadMap    | EUR/MWh |  30.32  |
| 2030DG     | co2       | TYNDP2018      | EUR/t   |  50     |
| 2030DG     | coal      | TYNDP2018      | EUR/MWh |   9.72  |
| 2030DG     | gas       | TYNDP2018      | EUR/MWh |  31.68  |
| 2030DG     | lignite   | TYNDP2018      | EUR/MWh |   3.96  |
| 2030DG     | mixed     | Own Assumption | EUR/MWh |   6.7   |
| 2030DG     | oil       | TYNDP2018      | EUR/MWh |  78.48  |
| 2030DG     | uranium   | TYNDP2018      | EUR/MWh |   1.692 |
| 2030DG     | waste     | Own Assumption | EUR/MWh |   6.7   |
| 2030NEPC   | biomass   | Own Assumption | EUR/MWh |   5     |
| 2030NEPC   | co2       | NEP2019        | EUR/t   |  29.4   |
| 2030NEPC   | coal      | NEP2019        | EUR/MWh |   8.4   |
| 2030NEPC   | gas       | NEP2019        | EUR/MWh |  26.4   |
| 2030NEPC   | lignite   | NEP2019        | EUR/MWh |   5.6   |
| 2030NEPC   | mixed     | Own Assumption | EUR/MWh |   6.7   |
| 2030NEPC   | oil       | NEP2019        | EUR/MWh |  48.3   |
| 2030NEPC   | uranium   | TYNDP2018      | EUR/MWh |   1.692 |
| 2030NEPC   | waste     | IRENA2015      | EUR/MWh |   6.7   |
| 2040DG     | biomass   | HeatRoadMap    | EUR/MWh |  30.32  |
| 2040DG     | co2       | TYNDP2018      | EUR/t   |  80     |
| 2040DG     | coal      | TYNDP2018      | EUR/MWh |  10.08  |
| 2040DG     | gas       | TYNDP2018      | EUR/MWh |  35.28  |
| 2040DG     | lignite   | TYNDP2018      | EUR/MWh |   3.96  |
| 2040DG     | mixed     | Own Assumption | EUR/MWh |   6.7   |
| 2040DG     | oil       | TYNDP2018      | EUR/MWh |  87.84  |
| 2040DG     | uranium   | TYNDP2018      | EUR/MWh |   1.692 |
| 2040DG     | waste     | Own Assumption | EUR/MWh |   6.7   |
| 2040GCA    | biomass   | HeatRoadMap    | EUR/MWh |  30.32  |
| 2040GCA    | co2       | TYNDP2018      | EUR/t   | 126     |
| 2040GCA    | coal      | TYNDP2018      | EUR/MWh |   6.48  |
| 2040GCA    | gas       | TYNDP2018      | EUR/MWh |  30.24  |
| 2040GCA    | lignite   | TYNDP2018      | EUR/MWh |   3.96  |
| 2040GCA    | mixed     | Own Assumption | EUR/MWh |   6.7   |
| 2040GCA    | oil       | TYNDP2018      | EUR/MWh |  50.22  |
| 2040GCA    | uranium   | TYNDP2018      | EUR/MWh |   1.692 |
| 2040GCA    | waste     | Own Assumption | EUR/MWh |   6.7   |
| 2050REF   | biomass   | HeatRoadMap    | EUR/MWh |  34.89  |
| 2050REF   | co2       | Own Assumption | EUR/t   | 150     |
| 2050REF   | coal      | HeatRoadMap    | EUR/MWh |   7.97  |
| 2050REF   | gas       | HeatRoadMap    | EUR/MWh |  43.72  |
| 2050REF   | lignite   | Own Assumption | EUR/MWh |   6     |
| 2050REF   | mixed     | Own Assumption | EUR/MWh |   6.7   |
| 2050REF   | oil       | HeatRoadMap    | EUR/MWh |  47.63  |
| 2050REF   | uranium   | Own Assumption | EUR/MWh |   1.692 |
| 2050REF   | waste     | Own Assumption | EUR/MWh |  30     |



\newpage
## Technical parameters

|   year | parameter    | carrier   | tech     | source                | unit      |      value |
|-------:|:-------------|:----------|:---------|:----------------------|:----------|-----------:|
|   2030 | capex        | gas       | ccgt     | DIW                   | Euro/kW   |  800       |
|   2030 | capex        | gas       | ocgt     | DIW                   | Euro/kW   |  400       |
|   2030 | capex        | lithium   | battery  | IWES                  | Euro/kW   |  785       |
|   2030 | capex        | solar     | pv       | DIW                   | Euro/kW   |  600       |
|   2030 | capex        | wind      | offshore | DIW                   | Euro/kW   | 2506       |
|   2030 | capex        | wind      | onshore  | DIW                   | Euro/kW   | 1182       |
|   2030 | capex_energy | cavern    | acaes    | IWES                  | Euro/kWh  |   40       |
|   2030 | capex_energy | hydrogen  | storage  | IWES                  | Euro/kWh  |    0.2     |
|   2030 | capex_energy | lithium   | battery  | IWES                  | Euro/kWh  |  300       |
|   2030 | capex_energy | redox     | battery  | IWES                  | Euro/kWh  |  150       |
|   2030 | capex_power  | cavern    | acaes    | IWES                  | Euro/kW   |  825       |
|   2030 | capex_power  | hydrogen  | storage  | IWES                  | Euro/kW   | 1550       |
|   2030 | capex_power  | lithium   | battery  | IWES                  | Euro/kW   |   65       |
|   2030 | capex_power  | redox     | battery  | IWES                  | Euro/kW   | 1000       |
|   2030 | efficiency   | biomass   | st       | DIW                   | per unit  |    0.35    |
|   2030 | efficiency   | cavern    | acaes    | IWES                  | per unit  |    0.7     |
|   2030 | efficiency   | coal      | st       | TYNDP2018             | per unit  |    0.4     |
|   2030 | efficiency   | gas       | ccgt     | TYNDP2018             | per unit  |    0.5     |
|   2030 | efficiency   | gas       | ocgt     | TYNDP2018             | per unit  |    0.38    |
|   2030 | efficiency   | hydro     | phs      | roundtrip; DIW        | per unit  |    0.75    |
|   2030 | efficiency   | hydro     | ror      | DIW                   | per unit  |    0.9     |
|   2030 | efficiency   | hydro     | rsv      | DIW                   | per unit  |    0.9     |
|   2030 | efficiency   | hydrogen  | storage  | IWES                  | per unit  |    0.32    |
|   2030 | efficiency   | lignite   | st       | TYNDP2018             | per unit  |    0.4     |
|   2030 | efficiency   | lithium   | battery  | IWES                  | per unit  |    0.9     |
|   2030 | efficiency   | mixed     | st       | Own assumption        | per unit  |    0.26    |
|   2030 | efficiency   | oil       | ocgt     | TYNDP2018             | per unit  |    0.35    |
|   2030 | efficiency   | porous    | acaes    | Own assumption (2050) | per unit  |    0.5     |
|   2030 | efficiency   | redox     | battery  | IWES                  | per unit  |    0.74    |
|   2030 | efficiency   | uranium   | st       | TYNDP2018             | per unit  |    0.33    |
|   2030 | efficiency   | waste     | st       | Own assumption        | per unit  |    0.26    |
|   2030 | fom          | cavern    | acaes    | Own assumption (2050) | Euro/kWha |   10       |
|   2030 | fom          | hydrogen  | storage  | Own assumption (2050) | Euro/kWha |   10       |
|   2030 | fom          | lithium   | battery  | Own assumption (2050) | Euro/kWha |   10       |
|   2030 | fom          | redox     | battery  | Own assumption (2050) | Euro/kWha |   10       |
|   2030 | lifetime     | cavern    | acaes    | IWES                  | a         |   30       |
|   2030 | lifetime     | hydrogen  | storage  | Own assumption        | a         |   22.5     |
|   2030 | lifetime     | lithium   | battery  | IWES                  | a         |   12       |
|   2030 | lifetime     | redox     | battery  | IWES                  | a         |   25       |
|   2030 | max_hours    | cavern    | acaes    | Own assumption (2050) | h         |    7       |
|   2030 | max_hours    | hydro     | phs      | Own assumption (2050) | h         |    8       |
|   2030 | max_hours    | hydrogen  | storage  | Own assumption (2050) | h         |  168       |
|   2030 | max_hours    | lithium   | battery  | Own assumption (2050) | h         |    6.5     |
|   2030 | max_hours    | porous    | acaes    | Own assumption (2050) | h         |  300       |
|   2030 | max_hours    | redox     | battery  | Own assumption (2050) | h         |    3.3     |
|   2030 | vom          | cavern    | acaes    | Own assumption (2050) | Euro/Mwh  |    1       |
|   2030 | vom          | hydrogen  | storage  | Own assumption (2050) | Euro/Mwh  |    1       |
|   2030 | vom          | lithium   | battery  | Own assumption (2050) | Euro/Mwh  |    1       |
|   2030 | vom          | redox     | battery  | Own assumption (2050) | Euro/Mwh  |    1       |
|   2040 | capex_energy | cavern    | acaes    | Own assumption (2050) | Euro/kWh  |   40       |
|   2040 | capex_energy | hydrogen  | storage  | Own assumption (2050) | Euro/kWh  |    0.2     |
|   2040 | capex_energy | lithium   | battery  | Own assumption (2050) | Euro/kWh  |  187       |
|   2040 | capex_energy | redox     | battery  | Own assumption (2050) | Euro/kWh  |   70       |
|   2040 | capex_power  | cavern    | acaes    | Own assumption (2050) | Euro/kW   |  750       |
|   2040 | capex_power  | hydrogen  | storage  | IWES 2050             | Euro/kW   | 1400       |
|   2040 | capex_power  | lithium   | battery  | Own assumption (2050) | Euro/kWh  |   35       |
|   2040 | capex_power  | redox     | battery  | Own assumption (2050) | Euro/kW   |  600       |
|   2040 | efficiency   | biomass   | st       | Own assumption        | per unit  |    0.4185  |
|   2040 | efficiency   | cavern    | acaes    | Own assumption (2050) | per unit  |    0.73    |
|   2040 | efficiency   | coal      | st       | Own assumption        | per unit  |    0.425   |
|   2040 | efficiency   | gas       | ccgt     | Own assumption        | per unit  |    0.53475 |
|   2040 | efficiency   | gas       | ocgt     | Own assumption        | per unit  |    0.373   |
|   2040 | efficiency   | hydro     | phs      | roundtrip; DIW        | per unit  |    0.75    |
|   2040 | efficiency   | hydro     | ror      | DIW                   | per unit  |    0.9     |
|   2040 | efficiency   | hydro     | rsv      | DIW                   | per unit  |    0.9     |
|   2040 | efficiency   | hydrogen  | storage  | Own assumption (2050) | per unit  |    0.46    |
|   2040 | efficiency   | lignite   | st       | Own assumption        | per unit  |    0.4     |
|   2040 | efficiency   | lithium   | battery  | Own assumption (2050) | per unit  |    0.92    |
|   2040 | efficiency   | mixed     | st       | Own assumption        | per unit  |    0.28    |
|   2040 | efficiency   | oil       | ocgt     | Own assumption        | per unit  |    0.373   |
|   2040 | efficiency   | porous    | acaes    | Own assumption (2050) | per unit  |    0.56    |
|   2040 | efficiency   | redox     | battery  | Own assumption (2050) | per unit  |    0.8     |
|   2040 | efficiency   | uranium   | st       | Own assumption        | per unit  |    0.335   |
|   2040 | efficiency   | waste     | st       | Own assumption        | per unit  |    0.26    |
|   2040 | fom          | cavern    | acaes    | Own assumption (2050) | Euro/kWha |   10       |
|   2040 | fom          | hydrogen  | storage  | Own assumption (2050) | Euro/kWha |   10       |
|   2040 | fom          | lithium   | battery  | Own assumption (2050) | Euro/kWha |   10       |
|   2040 | fom          | redox     | battery  | Own assumption (2050) | Euro/kWha |   10       |
|   2040 | lifetime     | cavern    | acaes    | Own assumption (2050) | a         |   30       |
|   2040 | lifetime     | hydrogen  | storage  | Own assumption (2050) | a         |   22.5     |
|   2040 | lifetime     | lithium   | battery  | Own assumption (2050) | a         |   20       |
|   2040 | lifetime     | redox     | battery  | Own assumption (2050) | a         |   25       |
|   2040 | max_hours    | cavern    | acaes    | Own assumption (2050) | h         |    7       |
|   2040 | max_hours    | hydro     | phs      | Own assumption (2050) | h         |    8       |
|   2040 | max_hours    | hydrogen  | storage  | Own assumption (2050) | h         |  168       |
|   2040 | max_hours    | lithium   | battery  | Own assumption (2050) | h         |    6.5     |
|   2040 | max_hours    | porous    | acaes    | Own assumption (2050) | h         |  300       |
|   2040 | max_hours    | redox     | battery  | Own assumption (2050) | h         |    3.3     |
|   2040 | vom          | cavern    | acaes    | Own assumption (2050) | Euro/Mwh  |    1       |
|   2040 | vom          | hydrogen  | storage  | Own assumption (2050) | Euro/Mwh  |    1       |
|   2040 | vom          | lithium   | battery  | Own assumption (2050) | Euro/Mwh  |    1       |
|   2040 | vom          | redox     | battery  | Own assumption (2050) | Euro/Mwh  |    1       |
|   2050 | avf          | biomass   | st       | Own assumption        | per unit  |    0.9     |
|   2050 | avf          | coal      | st       | PRIMES                | per unit  |    0.85    |
|   2050 | avf          | gas       | ccgt     | PRIMES                | per unit  |    0.85    |
|   2050 | avf          | gas       | ocgt     | PRIMES                | per unit  |    0.96    |
|   2050 | avf          | hydro     | phs      | Own assumption        | per unit  |    1       |
|   2050 | avf          | hydro     | ror      | Own assumption        | per unit  |    1       |
|   2050 | avf          | hydro     | rsv      | Own assumption        | per unit  |    1       |
|   2050 | avf          | lignite   | st       | PRIMES                | per unit  |    0.85    |
|   2050 | avf          | lithium   | battery  | Own assumption        | per unit  |    1       |
|   2050 | avf          | mixed     | st       | Own assumption        | per unit  |    0.9     |
|   2050 | avf          | oil       | ocgt     | PRIMES                | per unit  |    0.9     |
|   2050 | avf          | porous    | acaes    | Own assumption        | per unit  |    1       |
|   2050 | avf          | solar     | pv       | Own assumption        | per unit  |    1       |
|   2050 | avf          | uranium   | st       | Own assumption        | per unit  |    0.9     |
|   2050 | avf          | waste     | st       | Own assumption        | per unit  |    0.9     |
|   2050 | avf          | wind      | offshore | Own assumption        | per unit  |    1       |
|   2050 | avf          | wind      | onshore  | Own assumption        | per unit  |    1       |
|   2050 | capex        | biomass   | st       | DIW, p. 75            | Euro/kW   | 1951       |
|   2050 | capex        | coal      | st       | DIW, p. 75            | Euro/kW   | 1300       |
|   2050 | capex        | gas       | ccgt     | DIW, p. 75            | Euro/kW   |  800       |
|   2050 | capex        | gas       | ocgt     | DIW, p. 75            | Euro/kW   |  400       |
|   2050 | capex        | hydro     | phs      | DIW, p. 75            | Euro/kW   | 2000       |
|   2050 | capex        | hydro     | ror      | DIW, p. 75            | Euro/kW   | 3000       |
|   2050 | capex        | hydro     | rsv      | DIW, p. 75            | Euro/kW   | 2000       |
|   2050 | capex        | lignite   | st       | DIW, p. 75            | Euro/kW   | 1500       |
|   2050 | capex        | oil       | ocgt     | DIW, p. 75            | Euro/kW   |  400       |
|   2050 | capex        | solar     | pv       | DIW, p. 75            | Euro/kW   |  425       |
|   2050 | capex        | wind      | offshore | DIW, p. 75            | Euro/kW   | 2093       |
|   2050 | capex        | wind      | onshore  | DIW, p. 75            | Euro/kW   | 1075       |
|   2050 | capex_energy | cavern    | acaes    | Schill2018            | Euro/kWh  |   40       |
|   2050 | capex_energy | hydrogen  | storage  | Schill2018            | Euro/kWh  |    0.2     |
|   2050 | capex_energy | lithium   | battery  | Schill2018            | Euro/kWh  |  187       |
|   2050 | capex_energy | redox     | battery  | Schill2018            | Euro/kWh  |   70       |
|   2050 | capex_power  | cavern    | acaes    | Schill2018            | Euro/kW   |  750       |
|   2050 | capex_power  | hydrogen  | storage  | Schill2018            | Euro/kW   | 1000       |
|   2050 | capex_power  | lithium   | battery  | Schill2018            | Euro/kWh  |   35       |
|   2050 | capex_power  | redox     | battery  | Schill2018            | Euro/kW   |  600       |
|   2050 | efficiency   | biomass   | st       | DIW                   | per unit  |    0.487   |
|   2050 | efficiency   | cavern    | acaes    | roundtrip;Schill2018  | per unit  |    0.73    |
|   2050 | efficiency   | coal      | st       | DIW                   | per unit  |    0.45    |
|   2050 | efficiency   | gas       | ccgt     | Avg; DIW              | per unit  |    0.5695  |
|   2050 | efficiency   | gas       | ocgt     | Avg; DIW              | per unit  |    0.366   |
|   2050 | efficiency   | hydro     | phs      | roundtrip; DIW        | per unit  |    0.75    |
|   2050 | efficiency   | hydro     | ror      | DIW                   | per unit  |    0.9     |
|   2050 | efficiency   | hydro     | rsv      | DIW                   | per unit  |    0.9     |
|   2050 | efficiency   | hydrogen  | storage  | roundtrip;Schill2018  | per unit  |    0.46    |
|   2050 | efficiency   | lignite   | st       | Avg; DIW              | per unit  |    0.4     |
|   2050 | efficiency   | lithium   | battery  | roundtrip; Schill2018 | per unit  |    0.92    |
|   2050 | efficiency   | mixed     | st       | Own assumption        | per unit  |    0.3     |
|   2050 | efficiency   | oil       | ocgt     | DIW                   | per unit  |    0.396   |
|   2050 | efficiency   | porous    | acaes    | Own assumption        | per unit  |    0.56    |
|   2050 | efficiency   | redox     | battery  | roundtrip;Schill2018  | per unit  |    0.8     |
|   2050 | efficiency   | uranium   | st       | DIW                   | per unit  |    0.34    |
|   2050 | efficiency   | waste     | st       | Own assumption        | per unit  |    0.26    |
|   2050 | fom          | biomass   | st       | DIW, p.78             | Euro/kWa  |  100       |
|   2050 | fom          | cavern    | acaes    | Schill2018            | Euro/kWha |   10       |
|   2050 | fom          | coal      | st       | DIW, p.78             | Euro/kWa  |   25       |
|   2050 | fom          | gas       | ccgt     | DIW, p.78             | Euro/kWa  |   20       |
|   2050 | fom          | gas       | ocgt     | DIW, p.78             | Euro/kWa  |   15       |
|   2050 | fom          | hydro     | phs      | DIW, p.78             | Euro/kWa  |   20       |
|   2050 | fom          | hydro     | ror      | DIW, p.78             | Euro/kWa  |   60       |
|   2050 | fom          | hydro     | rsv      | DIW, p.78             | Euro/kWa  |   20       |
|   2050 | fom          | hydrogen  | storage  | Schill2018            | Euro/kWha |   10       |
|   2050 | fom          | lignite   | st       | DIW, p.78             | Euro/kWa  |   30       |
|   2050 | fom          | lithium   | battery  | Schill2018            | Euro/kWha |   10       |
|   2050 | fom          | oil       | ocgt     | DIW, p.78             | Euro/kWa  |    6       |
|   2050 | fom          | redox     | battery  | Schill2018            | Euro/kWha |   10       |
|   2050 | fom          | solar     | pv       | DIW, p.78             | Euro/kWa  |   25       |
|   2050 | fom          | wind      | offshore | DIW, p.78             | Euro/kWa  |   80       |
|   2050 | fom          | wind      | onshore  | DIW, p.78             | Euro/kWa  |   35       |
|   2050 | lifetime     | biomass   | st       | DIW, p. 72            | a         |   30       |
|   2050 | lifetime     | cavern    | acaes    | Schill2018            | a         |   30       |
|   2050 | lifetime     | coal      | st       | DIW, p. 72            | a         |   40       |
|   2050 | lifetime     | gas       | ccgt     | DIW, p. 72            | a         |   30       |
|   2050 | lifetime     | gas       | ocgt     | DIW, p. 72            | a         |   30       |
|   2050 | lifetime     | hydro     | phs      | DIW, p. 72            | a         |   50       |
|   2050 | lifetime     | hydro     | ror      | DIW, p. 72            | a         |   50       |
|   2050 | lifetime     | hydro     | rsv      | DIW, p. 72            | a         |   50       |
|   2050 | lifetime     | hydrogen  | storage  | Schill2018            | a         |   22.5     |
|   2050 | lifetime     | lignite   | st       | DIW, p. 72            | a         |   40       |
|   2050 | lifetime     | lithium   | battery  | Schill2018            | a         |   20       |
|   2050 | lifetime     | oil       | ocgt     | DIW, p. 72            | a         |   40       |
|   2050 | lifetime     | redox     | battery  | Schill2018            | a         |   25       |
|   2050 | lifetime     | solar     | pv       | DIW, p. 72            | a         |   25       |
|   2050 | lifetime     | wind      | offshore | DIW, p. 72            | a         |   25       |
|   2050 | lifetime     | wind      | onshore  | DIW, p. 72            | a         |   25       |
|   2050 | max_hours    | cavern    | acaes    | Wolf2011              | h         |    7       |
|   2050 | max_hours    | hydro     | phs      | Plessmann, p. 90      | h         |    8       |
|   2050 | max_hours    | hydrogen  | storage  | eGo                   | h         |  168       |
|   2050 | max_hours    | lithium   | battery  | Plessmann, p. 90      | h         |    6.5     |
|   2050 | max_hours    | porous    | acaes    | Own assumption        | h         |  300       |
|   2050 | max_hours    | redox     | battery  | ZNES                  | h         |    3.3     |
|   2050 | vom          | biomass   | st       | Own assumption        | Euro/Mwh  |   10       |
|   2050 | vom          | cavern    | acaes    | Schill2018            | Euro/Mwh  |    1       |
|   2050 | vom          | coal      | st       | DIW, p. 78            | Euro/Mwh  |    6       |
|   2050 | vom          | gas       | ccgt     | DIW, p. 78            | Euro/Mwh  |    4       |
|   2050 | vom          | gas       | ocgt     | DIW, p. 78            | Euro/Mwh  |    3       |
|   2050 | vom          | hydro     | phs      | DIW, p. 78            | Euro/Mwh  |    0       |
|   2050 | vom          | hydro     | ror      | DIW, p. 78            | Euro/Mwh  |    0       |
|   2050 | vom          | hydro     | rsv      | DIW, p. 78            | Euro/Mwh  |    0       |
|   2050 | vom          | hydrogen  | storage  | Schill2018            | Euro/Mwh  |    1       |
|   2050 | vom          | lignite   | st       | DIW, p. 78            | Euro/Mwh  |    7       |
|   2050 | vom          | lithium   | battery  | Schill2018            | Euro/Mwh  |    1       |
|   2050 | vom          | mixed     | st       | Own assumption        | Euro/Mwh  |    5       |
|   2050 | vom          | oil       | ocgt     | DIW, p. 78            | Euro/Mwh  |    3       |
|   2050 | vom          | redox     | battery  | Schill2018            | Euro/Mwh  |    1       |
|   2050 | vom          | solar     | pv       | Plessmann             | Euro/Mwh  |    0       |
|   2050 | vom          | uranium   | st       | DIW, p. 78, AVG       | Euro/Mwh  |    8.5     |
|   2050 | vom          | waste     | st       | Own assumption        | Euro/Mwh  |   10       |
|   2050 | vom          | wind      | offshore | Plessmann             | Euro/Mwh  |    0       |
|   2050 | vom          | wind      | onshore  | Plessmann             | Euro/Mwh  |    0       |


\newpage
## Installed capacities

The table show the installed grid capacities for path towards 100% renewable energy supply
from 2030 to 2050. For the 2030NEPC scenario, the 2030DG Grid has been applied.

![Installed transmission capacities in 2050](figures/grid-scenario2050REF.pdf){width=100%}

![Installed transmission capacities in 2040](figures/grid-scenario2040GCA.pdf){width=100%}

![Installed transmission capacities in 2040](figures/grid-scenario2040DG.pdf){width=100%}

![Installed transmission capacities in 2030](figures/grid-scenario2030DG.pdf){width=100%}

\newpage  
# Data Sources

All relevant raw input data can be found in:

* https://github.com/ZNES-datapackages/angus-input-data
* https://github.com/ZNES-datapackages/technology-potential
* https://zenodo.org/record/3549531

The scenario datapackages with python scripts and the model is located
on github:

* https://github.com/znes/angus-scenarios

# Links

* [ehighway website](https://www.entsoe.eu/outlooks/ehighways-2050/)
* [TYNDP2018a data](https://www.entsoe.eu/Documents/TYNDP%20documents/TYNDP2018/Scenarios%20Data%20Sets/Input%20Data.xlsx)
* [TYNDP2018b data](https://www.entsoe.eu/Documents/TYNDP%20documents/TYNDP2018/Scenarios%20Data%20Sets/ENTSO%20Scenario%202018%20Generation%20Capacities.xlsm)
* [NinjaWind data](https://www.renewables.ninja/static/downloads/ninja_europe_wind_v1.1.zip)
* [NinjaPV data](https://www.renewables.ninja/static/downloads/ninja_europe_pv_v1.1.zip)
* [OPSD demand data](https://data.open-power-system-data.org/time_series/2018-06-30/time_series_60min_singleindex.csv)
* [OPSD powerplant  data](https://data.open-power-system-data.org/conventional_power_plants/2018-12-20/conventional_power_plants_DE.csv)
* [OPSD heat data]("https://data.open-power-system-data.org/when2heat/opsd-when2heat-2019-08-06.zip")
* [NEP2019a](https://www.netzentwicklungsplan.de/sites/default/files/paragraphs-files/NEP_2030_V2019_2_Entwurf_Teil1.pdf)
* [NEP2019 powerplant data](https://www.netzentwicklungsplan.de/sites/default/files/paragraphs-files/Kraftwerksliste_%C3%9CNB_Entwurf_Szenariorahmen_2030_V2019_0_0.xlsx)
* [Restore2050 hydro data](https://zenodo.org/record/804244/#.XTcUhfyxUax)
* [Brown2018 sector coupling data](https://zenodo.org/record/1146666#.XTcTdvyxUaw)
* [hotmaps biomass data](https://gitlab.com/hotmaps/potential/potential_biomass)

# References
