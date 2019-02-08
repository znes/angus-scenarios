import os

import multiprocessing as mp

from oemof.tabular import datapackage
from fuchur.scripts import bus, capacity_factors, electricity, grid, biomass
from fuchur.cli import Scenario

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

    bus.add(config["buses"], datapackage_dir)

    biomass.add(config["buses"], datapackage_dir)

    grid.tyndp_grid(config["buses"]["electricity"], datapackage_dir)

    electricity.tyndp_load(
        config["buses"]["electricity"], config["tyndp"]["load"],
        datapackage_dir)

    electricity.opsd_load_profile(
        config["buses"]["electricity"],
        config["temporal"]["demand_year"],
        config["temporal"]["scenario_year"],
        datapackage_dir)

    electricity.tyndp_generation(
        set(config["buses"]["electricity"]) - set(['DE']),
        config['tyndp']['generation'],
        config["temporal"]["scenario_year"],
        datapackage_dir)

    electricity.nep_2019(
        config["temporal"]["scenario_year"],
        datapackage_dir)

    electricity.excess(datapackage_dir)

    electricity.shortage(datapackage_dir)

    electricity.hydro_generation(config, datapackage_dir)

    capacity_factors.pv(
        config["buses"]["electricity"],
        config["temporal"]["weather_year"],
        config["temporal"]["scenario_year"],
        datapackage_dir)

    capacity_factors.wind(
        config["buses"]["electricity"],
        config["temporal"]["weather_year"],
        config["temporal"]["scenario_year"],
        datapackage_dir)

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

    #build(scenarios[0])
    p = mp.Pool(4)
    p.map(build, scenarios)
