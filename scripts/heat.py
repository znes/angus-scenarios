import os
import pandas as pd
from datapackage import Package
from oemof.tabular.datapackage import building

# raw_data_path = os.path.join(os.path.expanduser("~"), "oemof-raw-data")
#
# config = building.read_build_config("scenarios/2030C.toml")
# config["buses"]["heat"]


def german_heat_system(heat_buses, weather_year, scenario, scenario_year,
                       datapackage_dir, raw_data_path):
    """
    """
    data = (
        pd.DataFrame(
            Package(
                "https://raw.githubusercontent.com/ZNES-datapackages/"
                "angus-input-data/master/capacities/datapackage.json"
            )
            .get_resource("german-heat-system")
            .read(keyed=True)
        )
        .set_index(["scenario", "year", "carrier", "tech"])
        .loc[(scenario, scenario_year)]
    )

    filepath = building.download_data(
        "https://data.open-power-system-data.org/when2heat/"
        "opsd-when2heat-2019-08-06.zip",
        directory=raw_data_path,
        unzip_file="opsd-when2heat-2019-08-06/"
    )


    df = pd.read_csv(
        os.path.join(filepath, "opsd-when2heat-2019-08-06", "when2heat.csv"),
        index_col=[0], parse_dates=True, sep=";")

    df = df[
        ~((df.index.month == 2) & (df.index.day == 29))
    ]

    elements = []
    sequences = {}

    weather_year = str(weather_year)

    el_buses = building.read_elements(
        "bus.csv",
        directory=os.path.join(datapackage_dir, "data/elements")
    )
    heat_demand_total = float(data.loc[("heat", "load-decentral"), "value"])
    c = "heat"
    for bustype, buses in heat_buses.items():
        for b in buses:
            heat_bus = "-".join([b, bustype, c, "bus"])
            peak_demand_heat = (
                (df.loc[weather_year][b + "_heat_demand_total"] /
                 df.loc[weather_year][b + "_heat_demand_total"].sum() *
                 heat_demand_total).max() * 1000
            )

            el_buses.loc[heat_bus] = [True, "heat", None, "bus"]

            profile_name = "-".join([b, bustype, c, "load", "profile"])
            elements.append(
                {
                    "name": "-".join([b, bustype, c, "load"]),
                    "type": "load",
                    "bus": heat_bus,
                    "amount": heat_demand_total * 1000, # GWh -> MWh
                    "profile": profile_name,
                    "carrier": c,
                }
            )

            elements.append(
                {
                    "name": "-".join([b, bustype, "hp"]),
                    "type": "conversion",
                    "to_bus": heat_bus,
                    "from_bus": "DE-electricity",
                    "capacity": peak_demand_heat * 1.1,
                    "efficiency": 3,
                    "carrier": "electricity",
                    "tech": "ground-hp"
                }
            )

            elements.append(
                {
                    "name": "-".join([b, bustype, c, "tes"]),
                    "type": "storage",
                    "bus": heat_bus,
                    "capacity": peak_demand_heat * 1.1,
                    "storage_capacity": peak_demand_heat * 1.1 * 5,
                    "efficiency": 0.99,
                    "loss": 0.05,
                    "carrier": "heat",
                    "tech": "tes-tank"
                }
            )

        sequences[profile_name] = (
            df.loc[weather_year][b + "_heat_demand_total"] /
            df.loc[weather_year][b + "_heat_demand_total"].sum())
        sequences_df = pd.DataFrame(sequences)
        sequences_df.index.name = "timeindex"
        sequences_df.index = building.timeindex(year=str(scenario_year))

    building.write_elements(
        "heat_load.csv",
        pd.DataFrame([i for i in elements if i["type"] == "load"]).set_index("name"),
        directory=os.path.join(datapackage_dir, "data/elements"),
    )

    building.write_elements(
        "heatpump.csv",
        pd.DataFrame([i for i in elements if i["type"] == "conversion"]).set_index("name"),
        directory=os.path.join(datapackage_dir, "data/elements"),
    )

    building.write_elements(
        "heat_storage.csv",
        pd.DataFrame([i for i in elements if i["type"] == "storage"]).set_index("name"),
        directory=os.path.join(datapackage_dir, "data/elements"),
    )

    building.write_elements(
        "bus.csv",
        el_buses,
        directory=os.path.join(datapackage_dir, "data/elements"),
        replace=True
    )

    building.write_sequences(
        "heat_load_profile.csv",
        sequences_df,
        directory=os.path.join(datapackage_dir, "data/sequences"),
    )
