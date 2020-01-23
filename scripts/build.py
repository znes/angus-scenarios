import os

import multiprocessing as mp
import pandas as pd
from datapackage import Package

from oemof.tabular import datapackage
import bus, capacity_factors, electricity, grid, biomass, load, hydro, heat
from fuchur.cli import Scenario
from prepare import raw_data_path


def build(config):
    """
    """

    datapackage_dir = os.path.join("datapackages", config["name"])

    if not os.path.exists(datapackage_dir):
        os.makedirs(datapackage_dir)

    datapackage.processing.clean(
        path=datapackage_dir, directories=["data", "resources"]
    )

    datapackage.building.initialize(config=config, directory=datapackage_dir)

    technologies = pd.DataFrame(
        Package(
            "https://raw.githubusercontent.com/ZNES-datapackages/"
            "angus-input-data/master/technology/datapackage.json"
        )
        .get_resource("technology")
        .read(keyed=True)
    ).set_index(["year", "parameter", "carrier", "tech"])

    bus.electricity(
        config["buses"]["electricity"], datapackage_dir, raw_data_path
    )

    biomass.add(config["buses"], datapackage_dir)

    if config["scenario"].get("DE_system") != "":
        # for all countries add german capacities based
        electricity.german_energy_system(
            datapackage_dir,
            raw_data_path,
            scenario_name=config["scenario"]["DE_system"],
            scenario_year=config["scenario"]["year"],
            cost_scenario=config["scenario"]["cost"],
            technologies=technologies,
            sensitivities=config.get("sensitivities"),
        )
        DE_set = set(["DE"])
    else:
        DE_set = set()

    if config["scenario"]["year"] == 2050:

        # for 2050 add the ehighway grid
        grid.ehighway(
            config["buses"]["electricity"],
            config["scenario"]["year"],
            config["scenario"]["grid_loss"],
            config["scenario"]["grid"],
            datapackage_dir,
            raw_data_path,
        )

        # for 2050 add the ehighway loads for all non-german countries
        load.ehighway(
            set(config["buses"]["electricity"]) - DE_set,
            config["scenario"]["year"],
            config["scenario"]["EU_load"],
            datapackage_dir,
            raw_data_path,
        )
        # for 2050 add the ehighway capacities capacity for all non-german
        electricity.ehighway_generation(
            set(config["buses"]["electricity"]) - DE_set,
            config["scenario"]["cost"],
            config["scenario"]["EU_generation"],
            datapackage_dir,
            raw_data_path,
        )

    elif config["scenario"]["year"] in [2030, 2040]:
        grid.tyndp(
            config["buses"]["electricity"],
            config["scenario"]["grid_loss"],
            config["scenario"]["grid"],
            datapackage_dir,
            raw_data_path,
        )

        load.tyndp(
            set(config["buses"]["electricity"]) - DE_set,
            config["scenario"]["EU_load"],
            datapackage_dir,
            raw_data_path,
        )

        electricity.tyndp_generation_2018(
            set(config["buses"]["electricity"]) - DE_set,
            config["scenario"]["EU_generation"],
            config["scenario"]["cost"],
            config["scenario"]["year"],
            datapackage_dir,
            raw_data_path
        )

    # the same for all scenarios
    load.opsd_profile(
        config["buses"]["electricity"],
        config["scenario"]["weather_year"],
        config["scenario"]["year"],
        datapackage_dir,
        raw_data_path,
    )

    if config["scenario"]["pv_profiles"] == "ninja":
        pv_profiles = capacity_factors.ninja_pv_profiles

    if config["scenario"]["onshore_profiles"] == "ninja":
        onshore_wind_profiles = capacity_factors.ninja_onshore_wind_profiles

    if config["scenario"]["offshore_profiles"] == "eGo":
        offshore_wind_profiles = capacity_factors.eGo_offshore_wind_profiles
    elif config["scenario"]["offshore_profiles"] == "ninja":
        offshore_wind_profiles = capacity_factors.ninja_offshore_wind_profiles
    else:
        pass

    hydro.generation(config, config["scenario"]["year"],
                     datapackage_dir, raw_data_path)

    pv_profiles(
        config["buses"]["electricity"],
        config["scenario"]["weather_year"],
        config["scenario"]["year"],
        datapackage_dir,
        raw_data_path,
    )

    onshore_wind_profiles(
        config["buses"]["electricity"],
        config["scenario"]["weather_year"],
        config["scenario"]["year"],
        datapackage_dir,
        raw_data_path,
    )

    offshore_wind_profiles(
        config["buses"]["electricity"],
        config["scenario"]["weather_year"],
        config["scenario"]["year"],
        datapackage_dir,
        raw_data_path,
    )

    electricity.excess(datapackage_dir)

    electricity.shortage(datapackage_dir)


    if config["buses"].get("heat"):
        heat.german_heat_system(
            config["buses"]["heat"],
            config["scenario"]["weather_year"],
            config["scenario"]["DE_system"],
            config["scenario"]["year"],
            datapackage_dir,
            raw_data_path)


    datapackage.building.infer_metadata(
        package_name=config["name"],
        foreign_keys={
            "bus": [
                "volatile",
                "dispatchable",
                "storage",
                "heat_storage",
                "heat_load",
                "load",
                "ror",
                "reservoir",
                "phs",
                "excess",
                "shortage",
                "commodity",
            ],
            "profile": ["load", "volatile", "ror", "reservoir", "heat_load"],
            "from_to_bus": ["link", "conversion", "heatpump"],
            "chp": [],
        },
        path=datapackage_dir,
    )


if __name__ == "__main__":
    # scenarios = [
    #     Scenario.from_path(os.path.join("scenarios", s))
    #     for s in os.listdir("scenarios")
    # ]
    # p = mp.Pool(10)
    # p.map(build, scenarios)

    build(Scenario.from_path(os.path.join("scenarios", "2030NEPC.toml")))
