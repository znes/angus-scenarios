# ANGUS2 Project Scenario Calculations

## Preparation

If you want to build the packages for scenarios all you need to do is run one
script.

### Requirements

To run the script, make sure the requirements e.g. via pip

    pip install --process-dependency-links -U -r requirements.txt

### Scope

The spatial resolution is at NUTS 0 level, thus on the level of national states.

### Build

To build the package locally run the python script

    python scripts/build.py

This will initialize all directories if they don't exist, (download raw data),
create the meta-data file. The output data are stored under:

    /datapackages

## Compute

To compute the datapackages run:

    python scripts/compute.py

  This will create a results directory with all results.


# Model assumptions

## Demand

* Demand profiles are calculated from the OPSD dataset of the ENTSOE
timeseries for the selected weather year
* The amount of Demand per country is based on TYNDP2016 EU2030 scenario.

## Conventional generation

* Generation capacities are selected for the vision 1,2,3,4 of the
TYNDP2016 per country.
* Fuel and CO2 costs are based on the TYNDP2016  
* Efficiencies are based on own assumptions
* `Others-non-res` are modelled with marginal costs of set to zero. The maximum
full load hours are set to 2000 h for these technologies
* All other conventional technologies are set to maximum of 85 % of there total
installed capacities.   

## Renewables

* Maximum biomass potential per country the hotmaps potential is used. The
installed capacity of biomass is assumed to be `biofuels` and `others-res`
from the TNYDP2016.
* Renewable capacities for wind and pv are based on the TYNDP2016
* For the renewable profiles of wind and pv timeseries of renewables ninja are used
* Hydro capacities are assumend to be the same as in 2015. The inflow in run of river and
reservoirs is modelled based on the inflow timeseries of the Restore2050 project.  
