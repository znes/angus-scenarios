import os
import pandas as pd
from oemof.tabular.datapackage import building

# raw_data_path = os.path.join(os.path.expanduser("~"), "oemof-raw-data")
#
# config = building.read_build_config("scenarios/2030C.toml")
# config["buses"]["heat"]


def load(heat_buses, weather_year, datapackage_dir, raw_data_path):
    """
    """
    filepath = building.download_data(
        "https://data.open-power-system-data.org/when2heat/opsd-when2heat-2019-08-06.zip",
        directory=raw_data_path,
        unzip_file="opsd-when2heat-2019-08-06/"
    )

    df = pd.read_csv(
        os.path.join(filepath, "opsd-when2heat-2019-08-06", "when2heat.csv"),
        index_col=[0], parse_dates=True, sep=";")

    elements = []
    sequences = {}

    weather_year = str(weather_year)

    c = "heat"
    for bustype, buses in heat_buses.items():
        for b in buses:
            profile_name = "-".join([b, bustype, c, "load", "profile"])
            elements.append(
                {
                    "name": "-".join([b, bustype, c, "load"]),
                    "type": "load",
                    "bus": "-".join([b, bustype, c]),
                    "amount": 200 * 1e6,
                    "profile": profile_name,
                    "carrier": c,
                }
            )

        sequences[profile_name] = (
            df.loc[weather_year][b + "_heat_demand_total"] /
            df.loc[weather_year][b + "_heat_demand_total"].sum())
        sequences_df = pd.DataFrame(sequences)
        sequences_df.index.name = "timeindex"

    building.write_elements(
        "heat_load.csv",
        pd.DataFrame(elements).set_index("name"),
        directory=os.path.join(datapackage_dir, "data/elements"),
    )

    building.write_sequences(
        "heat_load_profile.csv",
        sequences_df,
        directory=os.path.join(datapackage_dir, "data/sequences"),
    )


def decentral(
    config,
    datapackage_dir,
    heat_buses,
    techmap={
        "backpressure_decentral": "backpressure",
        "boiler_decentral": "dispatchable",
        "heatpump_decentral": "heatpump",
        "hotwatertank_decentral": "storage",
    },
):

    carrier_cost = (
        pd.DataFrame(
            carrier_package.get_resource("carrier-cost").read(keyed=True)
        )
        .set_index(["scenario", "carrier"])
        .sort_index()
    )

    emission_factors = (
        pd.DataFrame(
            carrier_package.get_resource("emission-factor").read(keyed=True)
        )
        .set_index(["carrier"])
        .sort_index()
    )

    elements = dict()

    for bustype, buses in heat_buses.items():
        for b in buses:
            for tech in techmap:
                element_name = b + "-" + tech

                heat_bus = "-".join([b, bustype, c])

                elements[element_name] = {}

                if techmap.get(tech) == "backpressure":
                    carrier = "gas"
                    element.update(
                        {
                            "type": techmap[tech],
                            "fuel_bus": "",
                            "carrier": carrier,
                            "fuel_cost": "",
                            "electricity_bus": b + "-electricity",
                            "heat_bus": heat_bus,
                            "thermal_efficiency": entry["thermal_efficiency"],
                            "input_parameters": json.dumps(
                                {
                                    "emission_factor": float(
                                        emission_factors.at[carrier, "value"]
                                    )
                                }
                            ),
                            "electric_efficiency": entry["electrical_efficiency"],
                            "tech": tech,

                        }
                    )

            elif techmap.get(tech) == "dispatchable":
                element.update(
                    {
                        "type": techmap[tech],
                        "carrier": entry["carrier"],
                        "marginal_cost": (
                            float(
                                carrier.at[(entry["carrier"], "cost"), "value"]
                            )
                            / float(entry["efficiency"])
                        ),
                        "bus": heat_bus,
                        "output_parameters": json.dumps(
                            {
                                "emission_factor": float(
                                    emission.at[
                                        (entry["carrier"], "emission-factor"),
                                        "value",
                                    ]
                                )
                                / float(entry["efficiency"])
                            }
                        ),
                        "capacity_potential": "Infinity",
                        "tech": tech,
                        "capacity_cost": annuity(
                            float(entry["capacity_cost"]),
                            float(entry["lifetime"]),
                            wacc,
                        )
                        * 1000,
                    }
                )

            elif techmap.get(tech) == "conversion":
                element.update(
                    {
                        "type": techmap[tech],
                        "carrier": entry["carrier"],
                        "from_bus": b + "-electricity",
                        "to_bus": heat_bus,
                        "efficiency": entry["efficiency"],
                        "capacity_potential": "Infinity",
                        "tech": tech,
                        "capacity_cost": annuity(
                            float(entry["capacity_cost"]),
                            float(entry["lifetime"]),
                            wacc,
                        )
                        * 1000,
                    }
                )

            elif techmap.get(tech) == "storage":
                element.update(
                    {
                        "storage_capacity_cost": annuity(
                            float(entry["storage_capacity_cost"]),
                            float(entry["lifetime"]),
                            wacc,
                        )
                        * 1000,
                        "bus": heat_bus,
                        "tech": tech,
                        "type": "storage",
                        "capacity_potential": "Infinity",
                        # rounttrip -> to in / out efficiency
                        "efficiency": float(entry["efficiency"]) ** 0.5,
                        "capacity_ratio": entry["capacity_ratio"],
                    }
                )

    elements = pd.DataFrame.from_dict(elements, orient="index")

    for type in set(techmap.values()):
        building.write_elements(
            type + ".csv",
            elements.loc[elements["type"] == type].dropna(how="all", axis=1),
            directory=os.path.join(datapackage_dir, "data", "elements"),
        )


def central(
    config,
    datapackage_dir,
    techmap={
        "extraction": "extraction",
        "boiler_central": "dispatchable",
        "hotwatertank_central": "storage",
        "heatpump_central": "conversion",
    },
):
    """
    """

    wacc = config["cost"]["wacc"]

    technology_cost = Package(
        "https://raw.githubusercontent.com/ZNES-datapackages/"
        "technology-cost/master/datapackage.json"
    )

    technologies = pd.DataFrame(
        technology_cost.get_resource("central_heat").read(keyed=True)
    )

    technologies = (
        technologies.groupby(["year", "tech", "carrier"])
        .apply(lambda x: dict(zip(x.parameter, x.value)))
        .reset_index("carrier")
        .apply(lambda x: dict({"carrier": x.carrier}, **x[0]), axis=1)
    )
    technologies = technologies.loc[
        config["temporal"]["scenario_year"]
    ].to_dict()

    carrier = pd.DataFrame(
        technology_cost.get_resource("carrier").read(keyed=True)
    ).set_index(["carrier", "parameter"])

    # maybe we should prepare emission factors for scenario year...
    emission = carrier[carrier.year == 2015]  # 2015 as emission not change

    carrier = carrier[carrier.year == config["temporal"]["scenario_year"]]

    elements = dict()

    for b in config["buses"]["heat"].get("central", []):
        for tech, entry in technologies.items():
            element_name = b + "-" + tech
            heat_bus = b + "-central-heat"

            element = entry.copy()

            elements[element_name] = element

            if techmap.get(tech) == "extraction":
                element.update(
                    {
                        "type": techmap[tech],
                        "carrier": entry["carrier"],
                        "fuel_bus": "GL-" + entry["carrier"],
                        "carrier_cost": carrier.at[
                            (entry["carrier"], "cost"), "value"
                        ],
                        "electricity_bus": "DE-electricity",
                        "heat_bus": heat_bus,
                        "thermal_efficiency": entry["thermal_efficiency"],
                        "input_parameters": json.dumps(
                            {
                                "emission_factor": float(
                                    emission.at[
                                        (entry["carrier"], "emission-factor"),
                                        "value",
                                    ]
                                )
                            }
                        ),
                        "electric_efficiency": entry["electrical_efficiency"],
                        "condensing_efficiency": entry[
                            "condensing_efficiency"
                        ],
                        "capacity_potential": "Infinity",
                        "tech": tech,
                        "capacity_cost": annuity(
                            float(entry["capacity_cost"]),
                            float(entry["lifetime"]),
                            wacc,
                        )
                        * 1000,
                    }
                )

            elif techmap.get(tech) == "backpressure":
                element.update(
                    {
                        "type": techmap[tech],
                        "fuel_bus": "GL-" + entry["carrier"],
                        "carrier": entry["carrier"],
                        "fuel_cost": carrier.at[
                            (entry["carrier"], "cost"), "value"
                        ],
                        "electricity_bus": b + "-electricity",
                        "heat_bus": heat_bus,
                        "thermal_efficiency": entry["thermal_efficiency"],
                        "input_parameters": json.dumps(
                            {
                                "emission_factor": float(
                                    emission.at[
                                        (entry["carrier"], "emission-factor"),
                                        "value",
                                    ]
                                )
                            }
                        ),
                        "electric_efficiency": entry["electrical_efficiency"],
                        "capacity_potential": "Infinity",
                        "tech": tech,
                        "capacity_cost": annuity(
                            float(entry["capacity_cost"]),
                            float(entry["lifetime"]),
                            wacc,
                        )
                        * 1000,  # €/kW -> €/MW
                    }
                )

            elif techmap.get(tech) == "dispatchable":
                element.update(
                    {
                        "type": techmap[tech],
                        "carrier": entry["carrier"],
                        "marginal_cost": (
                            float(
                                carrier.at[(entry["carrier"], "cost"), "value"]
                            )
                            / float(entry["efficiency"])
                        ),
                        "bus": heat_bus,
                        "output_parameters": json.dumps(
                            {
                                "emission_factor": float(
                                    emission.at[
                                        (entry["carrier"], "emission-factor"),
                                        "value",
                                    ]
                                )
                                / float(entry["efficiency"])
                            }
                        ),
                        "capacity_potential": "Infinity",
                        "tech": tech,
                        "capacity_cost": annuity(
                            float(entry["capacity_cost"]),
                            float(entry["lifetime"]),
                            wacc,
                        )
                        * 1000,
                    }
                )

            elif techmap.get(tech) == "conversion":
                element.update(
                    {
                        "type": techmap[tech],
                        "carrier": entry["carrier"],
                        "from_bus": b + "-electricity",
                        "to_bus": heat_bus,
                        "efficiency": entry["efficiency"],
                        "capacity_potential": "Infinity",
                        "tech": tech,
                        "capacity_cost": annuity(
                            float(entry["capacity_cost"]),
                            float(entry["lifetime"]),
                            wacc,
                        )
                        * 1000,
                    }
                )

            elif techmap.get(tech) == "storage":
                element.update(
                    {
                        "storage_capacity_cost": annuity(
                            float(entry["storage_capacity_cost"]),
                            float(entry["lifetime"]),
                            wacc,
                        )
                        * 1000,
                        "bus": heat_bus,
                        "tech": tech,
                        "type": "storage",
                        "capacity_potential": "Infinity",
                        # rounttrip -> to in / out efficiency
                        "efficiency": float(entry["efficiency"]) ** 0.5,
                        "capacity_ratio": entry["capacity_ratio"],
                    }
                )

    elements = pd.DataFrame.from_dict(elements, orient="index")

    for type in set(techmap.values()):
        building.write_elements(
            type + ".csv",
            elements.loc[elements["type"] == type].dropna(how="all", axis=1),
            directory=os.path.join(datapackage_dir, "data", "elements"),
        )
