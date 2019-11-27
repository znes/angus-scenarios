import os

import multiprocessing as mp

from oemof.tabular import datapackage
import bus, capacity_factors, electricity, grid, biomass, load, hydro, manipulate
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

    bus.electricity(
        config["buses"]["electricity"], datapackage_dir, raw_data_path
    )

    biomass.add(config["buses"], datapackage_dir)

    # must come before generation of others because later manipulation below...
    hydro.generation(config, datapackage_dir, raw_data_path)


    if config["scenario"]["year"] > 2035:
        grid.ehighway(
            config["buses"]["electricity"],
            config["scenario"]["year"],
            config["scenario"]["grid_loss"],
            config["scenario"]["grid"],
            datapackage_dir,
            raw_data_path,
        )

        load.ehighway(
            config["buses"]["electricity"],
            config["scenario"]["year"],
            config["scenario"]["EU_load"],
            datapackage_dir,
            raw_data_path,
        )

        electricity.ehighway_generation(
            config["buses"]["electricity"],
            config["scenario"]["cost"],
            config["scenario"]["EU_generation"],
            datapackage_dir,
            raw_data_path,
        )

    else:
        grid.tyndp(
            config["buses"]["electricity"],
            config["scenario"]["grid_loss"],
            datapackage_dir,
            raw_data_path,
        )

        load.tyndp(
            config["buses"]["electricity"],
            config["scenario"]["EU_load"],
            datapackage_dir,
            raw_data_path,
        )

        electricity.tyndp_generation_2018(
            set(config["buses"]["electricity"]) - set(["DE"]),
            config["scenario"]["EU_generation"],
            config["scenario"]["cost"],
            datapackage_dir,
            raw_data_path,
        )

        electricity.DE_nep_conventional(
            datapackage_dir,
            nep_scenario=config["scenario"]["DE_system"],
            cost_scenario=config["scenario"]["cost"],
            raw_data_path=raw_data_path,
        )

        electricity.DE_nep(
            datapackage_dir,
            raw_data_path,
            nep_scenario=config["scenario"]["DE_system"],
            cost_scenario=config["scenario"]["cost"],
        )

    load.opsd_profile(
        config["buses"]["electricity"],
        config["scenario"]["weather_year"],
        config["scenario"]["year"],
        datapackage_dir,
        raw_data_path,
    )

    if config["scenario"]["renewable_profiles"] == "ninja":
        pv_profiles = capacity_factors.ninja_pv_profiles
        wind_profiles = capacity_factors.ninja_wind_profiles
    elif config["scenario"]["renewable_profiles"] == "emhires":
        pv_profiles = capacity_factors.emhires_pv_profiles
        wind_profiles = capacity_factors.emhires_wind_profiles
    else:
        pass

    pv_profiles(
        config["buses"]["electricity"],
        config["scenario"]["weather_year"],
        config["scenario"]["year"],
        datapackage_dir,
        raw_data_path,
    )

    wind_profiles(
        config["buses"]["electricity"],
        config["scenario"]["weather_year"],
        config["scenario"]["year"],
        datapackage_dir,
        raw_data_path,
    )

    electricity.excess(datapackage_dir)

    electricity.shortage(datapackage_dir)

    manipulate.storage(
        config["name"],
        config["scenario"]["year"],
        datapackage_dir,
        raw_data_path,
    )


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
            "profile": ["load", "volatile", "ror", "reservoir"],
            "from_to_bus": ["link", "conversion"],
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

    #build(Scenario.from_path(os.path.join("scenarios", "2030C.toml")))
