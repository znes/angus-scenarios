
import os

import multiprocessing as mp

from oemof.tabular import datapackage
from fuchur.scripts import (bus, capacity_factors, electricity, grid, biomass,
                            load, hydro)
from fuchur.cli import Scenario

import fuchur

# set raw data path to the default fuchur raw raw_data_path
# which is: 'home/user/fuchur-raw-data'
# change this if you have your raw data stored somewhere else
raw_data_path = fuchur.__RAW_DATA_PATH__

def build(config):
    """
    """

    datapackage_dir = os.path.join("datapackages", config["name"])

    if not os.path.exists(datapackage_dir):
        os.makedirs(datapackage_dir)

    datapackage.processing.clean(
        path=datapackage_dir, directories=["data", "resources"]
    )

    datapackage.building.initialize(
        config=config, directory=datapackage_dir
    )

    bus.electricity(
        config["buses"]["electricity"],
        datapackage_dir,
        raw_data_path)

    biomass.add(config["buses"], datapackage_dir)

    grid.tyndp(
        config["buses"]["electricity"],
        datapackage_dir,
        raw_data_path)

    load.tyndp(
        config["buses"]["electricity"],
        config["tyndp"]["load"],
        datapackage_dir,
        raw_data_path)

    load.opsd_profile(
        config["buses"]["electricity"],
        config["temporal"]["demand_year"],
        config["temporal"]["scenario_year"],
        datapackage_dir,
        raw_data_path)

    electricity.tyndp_generation(
        set(config["buses"]["electricity"]) - set(['DE']),
        config['tyndp']['generation'],
        config["temporal"]["scenario_year"],
        datapackage_dir,
        raw_data_path)

    electricity.nep_2019(
        config["temporal"]["scenario_year"],
        datapackage_dir,
        scenario="B2030",
        bins=2,
        eaf=0.95,
        raw_data_path=raw_data_path)

    electricity.excess(datapackage_dir)

    electricity.shortage(datapackage_dir)

    hydro.generation(config, datapackage_dir, raw_data_path)

    capacity_factors.pv(
        config["buses"]["electricity"],
        config["temporal"]["weather_year"],
        config["temporal"]["scenario_year"],
        datapackage_dir,
        raw_data_path)

    capacity_factors.wind(
        config["buses"]["electricity"],
        config["temporal"]["weather_year"],
        config["temporal"]["scenario_year"],
        datapackage_dir,
        raw_data_path)

    datapackage.building.infer_metadata(
        package_name=config["name"],
        foreign_keys={
            "bus": [
                "volatile",
                "dispatchable",
                "storage",
                "load",
                "ror",
                "reservoir",
                "phs",
                "excess",
                "shortage",
                "commodity",
            ],
            "profile": [
                "load",
                "volatile",
                "ror",
                "reservoir"#
            ],
            "from_to_bus": [
                "link",
                "conversion"
            ],
            "chp": [],
        },
        path=datapackage_dir,
    )


if __name__ == "__main__":
    scenarios= [
        Scenario.from_path(os.path.join('scenarios', s))
        for s in os.listdir('scenarios')]
    p = mp.Pool(10)
    p.map(build, scenarios)

    #build(Scenario.from_path(os.path.join('scenarios', 'V4-2010.toml')))
