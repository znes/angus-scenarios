# ANGUS2 Project Scenario Calculations

## Preparation

If you want to build the packages for scenarios all you need to do is run one
script.

### Requirements

To run the script, make sure the requirements e.g. via pip

    pip install  -U -r requirements.txt

In addition for some plot `plotly-orca`. Installation instructions can
found here: https://github.com/plotly/orca

### Raw data

To run the build script the required raw data needs to be downloaded. Store the
data in your home directory under `fuchur-raw-data`. This dire


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

# Model assumptions

The Model is based on the NEP2030.  


## Demand

* Demand profiles are calculated from the OPSD dataset of the ENTSOE
timeseries for the selected weather year (2012)
* German demand is based on the NEP2030 scenarios (A2030, B2030, C2030)
* The amount of demand of the neigbouring countries is based on the TYNDP2016
scenario for 2030 'Sustainable Transition'


## Conventional generation

* Generation capacities are based on for the Vision 4 of the
TYNDP2016 for neigbouring countries
* German generation is derived from the NEP2030 scenarios
* Efficiencies are based on own assumptions for non-german countries. For
germany the OPSD powerplant register is used to calculate efficiencies for
the conventional powerplants in 2030
* Costs are based on the TYNDP cost assumptions
* `Others-non-res` are modelled with marginal costs of set to zero and
with max. fulloadhours of 2000h
* Waste is modelled with maximum of 2500h max. fulloadhours

## Renewables

* Maximum biomass potential per country the hotmaps potential is used. The
installed capacity of biomass is assumed to be `biofuels` and `others-res`
from the TNYDP2016.
* Renewable capacities for wind and pv are based on the TYNDP2016 for non german
countries.
* For the renewable profiles of wind and pv timeseries of renewables ninja are used
* Hydro capacities are assumend to be the same as in 2015. The inflow in run of river and
reservoirs is modelled based on the inflow timeseries of the Restore2050 project.  
