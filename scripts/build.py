
import os

import multiprocessing as mp

from oemof.tabular import datapackage
import bus, capacity_factors, electricity, grid, biomass, load, hydro
from fuchur.cli import Scenario


# set raw data path to the default fuchur raw raw_data_path
# which is: 'home/user/fuchur-raw-data'
# change this if you have your raw data stored somewhere else
raw_data_path = os.path.join(os.path.expanduser('~'), 'fuchur-raw-data')

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

    if config["temporal"]["scenario_year"] > 2035:
        grid.ehighway(
            config["buses"]["electricity"],
            config["temporal"]["scenario_year"],
            config["grid"]["loss"],
            datapackage_dir,
            config["ehighway"]["scenario"],
            raw_data_path)

        load.ehighway(
                config["buses"]["electricity"],
                config["temporal"]["scenario_year"],
                datapackage_dir,
                config["ehighway"]["scenario"],
                raw_data_path)

        electricity.ehighway_generation(
            config["buses"]["electricity"],
            config["availability_factor"],
            config["efficiencies"],
            config["temporal"]["scenario_year"],
            datapackage_dir,
            config["ehighway"]["scenario"],
            raw_data_path)

    else:
        grid.tyndp(
            config["buses"]["electricity"],
            config["grid"]["loss"],
            datapackage_dir,
            raw_data_path)

        load.tyndp(
            config["buses"]["electricity"],
            config["tyndp"]["load"],
            datapackage_dir,
            raw_data_path)

        electricity.tyndp_generation(
            set(config["buses"]["electricity"]) - set(['DE']),
            config["availability_factor"],
            config['tyndp']['generation'],
            config["temporal"]["scenario_year"],
            config['tyndp']["cost"],
            config["efficiencies"],
            config["max_fulloadhours"],
            datapackage_dir,
            raw_data_path)

        electricity.DE_nep_conventional(
            config["temporal"]["scenario_year"],
            datapackage_dir,
            scenario=config["nep_scenario"],
            bins=1,
            avf=0.95,
            max_fulloadhours=config["max_fulloadhours"],
            cost_scenario=config['tyndp']['cost'],
            raw_data_path=raw_data_path)

        electricity.DE_nep(
            datapackage_dir,
            raw_data_path,
            nep_scenario=config["nep_scenario"],
            efficiencies=config["efficiencies"])

    hydro.generation(config, datapackage_dir, raw_data_path)


    load.opsd_profile(
        config["buses"]["electricity"],
        config["temporal"]["demand_year"],
        config["temporal"]["scenario_year"],
        datapackage_dir,
        raw_data_path)

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

    electricity.excess(datapackage_dir)

    electricity.shortage(datapackage_dir)

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
                "reservoir"
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
    #p = mp.Pool(10)
    #p.map(build, scenarios)

    build(Scenario.from_path(os.path.join('scenarios', 'NEP2030-C.toml')))
