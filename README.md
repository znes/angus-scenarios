# ANGUS2 Project Scenario Calculations

## Preparation

If you want to build the packages for scenarios all you need to do is run some
scripts. Clone the directory and `cd` to the root diectory. From here all commands
are to be executed from the console.

### Requirements

To run the script, make sure the requirements e.g. via pip

    pip install  -U -r requirements.txt

In addition for some plots `plotly-orca`. Installation instructions can
found here: [orca](https://github.com/plotly/orca)

### Raw data

To run the build script the required raw data needs to be downloaded. Store the
data in your home directory under `oemof-raw-data`. The required data sets can
be found in the sources.


## Build

To build the package locally run the python script

    python scripts/build.py

This will initialize all directories if they don't exist, (download raw data),
create the meta-data file. The output data are stored under:

    /datapackages

### Configuration build files

The datapackages are build with the provided .toml-files provided in the
`/scenarios` folder. You can adapt the configuration files or add new ones to
your needs. All datapackages are build in parallel. If you want to build single
datapackages you can use the `build.py` function.


## Compute

To compute the datapackages run:

    python scripts/compute.py

  This will create a results directory with all results.

### Existing Datapackages

**The provided datapackages in the datapackage directory of this repository
may be outdated. Therefore you should rebuild the datapackages based on the provided
`scripts/build.py` script.**


## Plots

Plots can be generated by:

    python scripts/analysis.py


# Model assumptions

The Model is based on the NEP2030 version 2019.  


## Demand

* Demand profiles are calculated from the OPSD dataset of the ENTSOE
timeseries for the selected weather year.
* German demand is based on the NEP2030 scenarios (A2030, B2030, C2030)
* The amount of demand of the neigbouring countries is based on the TYNDP2018
scenario for 2030 'Sustainable Transition'. For the NEP2030C, the TYNDP
*Vision 2030 DG* has been chosen, for NEP2030C *VisionEU* has been used.


## Conventional generation

* Generation capacities are based on for the Vision 2030DG and 2030 EUCO of the TYNDP2018 for neigbouring countries
* German generation is derived from the NEP2030 scenarios
* Efficiencies are based on own assumptions for non-german countries. However,
the data of the TYNDP2018 has been used as a foundation. For
germany the OPSD powerplant register is used to calculate efficiencies for
the conventional powerplants in 2030.
* Costs are based on the NEP2030C and TYNDP cost assumptions

## Renewables

* Maximum biomass potential per country the hotmaps potential is used. The
installed capacity of biomass is assumed to be `biofuels` and `others-res`
from the TNYDP2018.
* Renewable capacities for wind and pv are based on the TYNDP2018 for non german
countries.
* For the renewable profiles of wind and pv timeseries of renewables ninja has
been used.
* Hydro capacities are assumend to be the same as in 2015. The inflow in run of river and
reservoirs is modelled based on the inflow timeseries of the Restore2050 project.

## Must Run

CHP Power plant smaller 10MW are modelled as must-run with a seasonal profile.



# Data Sources

* [TYNDP2018a](https://www.entsoe.eu/Documents/TYNDP%20documents/TYNDP2018/Scenarios%20Data%20Sets/Input%20Data.xlsx)
* [TYNDP2018b](https://www.entsoe.eu/Documents/TYNDP%20documents/TYNDP2018/Scenarios%20Data%20Sets/ENTSO%20Scenario%202018%20Generation%20Capacities.xlsm)
* [NinjaWind](https://www.renewables.ninja/static/downloads/ninja_europe_wind_v1.1.zip)
* [NinjaPV]("https://www.renewables.ninja/static/downloads/ninja_europe_pv_v1.1.zip")
* [OPSDa](https://data.open-power-system-data.org/time_series/2018-06-30/time_series_60min_singleindex.csv)
* [OPSDb](https://data.open-power-system-data.org/conventional_power_plants/2018-12-20/conventional_power_plants_DE.csv)
* [NEP2019a](https://www.netzentwicklungsplan.de/sites/default/files/paragraphs-files/NEP_2030_V2019_2_Entwurf_Teil1.pdf)
* [NEP2019b](https://www.netzentwicklungsplan.de/sites/default/files/paragraphs-files/Kraftwerksliste_%C3%9CNB_Entwurf_Szenariorahmen_2030_V2019_0_0.xlsx)
* [Restore2050](https://zenodo.org/record/804244/#.XTcUhfyxUax)
* [Brown](https://zenodo.org/record/1146666#.XTcTdvyxUaw)
