# ANGUS2 Project Scenario Calculations

## Preparation

If you want to build the packages for scenarios all you need to do is run some
scripts. Clone the directory and `cd` to the root diectory. From here all
commands are to be executed from the console.

### Requirements

To run the script, make sure the requirements e.g. via pip

    pip install  -U -r requirements.txt

In addition for some plots `plotly-orca`. Installation instructions can
found here: [orca](https://github.com/plotly/orca)

### Raw data

To run the build script the required raw data needs to be downloaded. Generally,
the data will be downloaded automatically. You have to create an  `oemof-raw-data`
directory in your home folder:


    mkdir /home/user/oemof-raw-data

If raw data does not exist run:

    python scripts/prepare.py

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
