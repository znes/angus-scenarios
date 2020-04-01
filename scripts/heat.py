import os
import pandas as pd
from datapackage import Package
from oemof.tabular.datapackage import building
import locale

from locale import atof

# raw_data_path = os.path.join(os.path.expanduser("~"), "oemof-raw-data")
#
# config = building.read_build_config("scenarios/2030C.toml")
# config["buses"]["heat"]

from oemof.tools.economics import annuity


def german_heat_system(
    heat_buses,
    weather_year,
    scenario,
    scenario_year,
    wacc,
    decentral_heat_flex_share,
    sensitivities,
    datapackage_dir,
    raw_data_path,
):
    """
    """
    technologies = pd.DataFrame(
        # Package('/home/planet/data/datapackages/technology-cost/datapackage.json')
        Package(
            "https://raw.githubusercontent.com/ZNES-datapackages/"
            "angus-input-data/master/technology/datapackage.json"
        )
        .get_resource("heat")
        .read(keyed=True)
    ).set_index(["year", "parameter", "carrier", "tech"])

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
        unzip_file="opsd-when2heat-2019-08-06/",
    )

    df = pd.read_csv(
        os.path.join(filepath, "opsd-when2heat-2019-08-06", "when2heat.csv"),
        index_col=[0],
        parse_dates=True,
        sep=";",
    )

    cop =  pd.read_csv(
        os.path.join(filepath, "opsd-when2heat-2019-08-06", "when2heat.csv"),
        decimal=",",
        index_col=[0],
        parse_dates=True,
        sep=";",
    )

    df = df[~((df.index.month == 2) & (df.index.day == 29))]
    cop = cop[~((cop.index.month == 2) & (cop.index.day == 29))]

    data["country"] = "DE"
    data.set_index("country", append=True, inplace=True)
    if sensitivities is not None:
        for k, v in sensitivities.items():
            k = k.split("-")
            data.at[(k[1], k[2], k[0]), "value"] = v

    elements = []
    sequences = {}

    weather_year = str(weather_year)


    gshp_cop = (
        cop.loc[
            weather_year,
            ["DE_COP_GSHP_floor", "DE_COP_GSHP_radiator", "DE_COP_GSHP_water"],
        ]
        .mean(axis=1)
    )
    ashp_cop = (
        cop.loc[
            weather_year,
            ["DE_COP_ASHP_floor", "DE_COP_ASHP_radiator", "DE_COP_ASHP_water"],
        ]
        .mean(axis=1)
    )

    el_buses = building.read_elements(
        "bus.csv", directory=os.path.join(datapackage_dir, "data/elements")
    )
    heat_demand_total = (
        float(data.loc[("decentral_heat", "load"), "value"]) * 1000
    )  # MWh
    for bustype, buses in heat_buses.items():
        carrier = bustype + "_heat"

        for b in buses:
            heat_bus = "-".join([b, carrier, "bus"])
            flex_peak_demand_heat = (
                df.loc[weather_year][b + "_heat_demand_total"]
                / df.loc[weather_year][b + "_heat_demand_total"].sum()  # MW
                * heat_demand_total
            ).max() * decentral_heat_flex_share

            peak_demand_heat = (
                df.loc[weather_year][b + "_heat_demand_total"]
                / df.loc[weather_year][b + "_heat_demand_total"].sum()  # MW
                * heat_demand_total
            ).max() * (1 - decentral_heat_flex_share)

            el_buses.loc[heat_bus] = [True, "heat", None, "bus"]

            profile_name = "-".join([b, carrier, "load", "profile"])

            if "flex" in bustype:
                elements.append(
                    {
                        "name": "-".join([b, carrier, "load"]),
                        "type": "load",
                        "bus": heat_bus,
                        "amount": heat_demand_total
                        * decentral_heat_flex_share,
                        "profile": profile_name,
                        "carrier": carrier,
                    }
                )
                elements.append(
                    {
                        "name": "-".join([b, carrier, "gshp"]),
                        "type": "conversion",
                        "to_bus": heat_bus,
                        "capacity_cost": (
                            float(
                                technologies.loc[
                                    (2050, "fom", "decentral_heat", "gshp"),
                                    "value",
                                ]
                            )
                            + annuity(
                                float(
                                    technologies.loc[
                                        (
                                            2050,
                                            "capex",
                                            "decentral_heat",
                                            "gshp",
                                        ),
                                        "value",
                                    ]
                                ),
                                float(
                                    technologies.loc[
                                        (
                                            2050,
                                            "lifetime",
                                            "decentral_heat",
                                            "gshp",
                                        ),
                                        "value",
                                    ]
                                ),
                                wacc,
                            )
                            * 1000,  # €/kW -> €/MW
                        )[0],
                        "from_bus": "DE-electricity",
                        "expandable": True,
                        "capacity": flex_peak_demand_heat,
                        "efficiency": "DE-gshp-profile",
                        "carrier": carrier,
                        "tech": "gshp",
                    }
                )

                name = "-".join([b, carrier, "tes"])
                if sensitivities is not None:
                    if name in sensitivities.keys():
                        capacity = sensitivities[name]
                    else:
                        capacity = flex_peak_demand_heat
                else:
                    capacity = flex_peak_demand_heat

                carrier = carrier.replace("flex-", "")
                elements.append(
                    {
                        "name": name,
                        "type": "storage",
                        "bus": heat_bus,
                        # "capacity": capacity,
                        "capacity_cost": float(
                            technologies.loc[
                                (2050, "fom", "decentral_heat", "tes"), "value"
                            ]
                        )
                        * 1000,
                        "storage_capacity_cost": (
                            annuity(
                                float(
                                    technologies.loc[
                                        (
                                            2050,
                                            "capex",
                                            "decentral_heat",
                                            "tes",
                                        ),
                                        "value",
                                    ]
                                ),
                                float(
                                    technologies.loc[
                                        (
                                            2050,
                                            "lifetime",
                                            "decentral_heat",
                                            "tes",
                                        ),
                                        "value",
                                    ]
                                ),
                                wacc,
                            )
                            * 1000,  # €/kWh -> €/MWh
                        )[0],
                        "expandable": True,
                        # "storage_capacity": capacity * float(technologies.loc[
                        #     (2050, "max_hours", carrier, "tes"),
                        #     "value"
                        # ]),
                        "efficiency": float(
                            technologies.loc[
                                (2050, "efficiency", carrier, "tes"), "value"
                            ]
                        )
                        ** 0.5,  # rountrip conversion
                        "loss": technologies.loc[
                            (2050, "loss", carrier, "tes"), "value"
                        ],
                        "marginal_cost": 0.001, 
                        "carrier": carrier,
                        "tech": "tes",
                    }
                )
            else:
                elements.append(
                    {
                        "name": "-".join([b, carrier, "load"]),
                        "type": "load",
                        "bus": heat_bus,
                        "amount": heat_demand_total
                        * (1 - decentral_heat_flex_share),
                        "profile": profile_name,
                        "carrier": carrier,
                    }
                )
                elements.append(
                    {
                        "name": "-".join([b, carrier, "gshp"]),
                        "type": "conversion",
                        "to_bus": heat_bus,
                        "capacity_cost": 0,
                        "expandable": False,
                        "from_bus": "DE-electricity",
                        "capacity": peak_demand_heat * 1.1,
                        "efficiency": "DE-gshp-profile",
                        "carrier": carrier,
                        "tech": "gshp",
                    }
                )

        sequences[profile_name] = (
            df.loc[weather_year][b + "_heat_demand_total"]
            / df.loc[weather_year][b + "_heat_demand_total"].sum()
        )
        sequences_df = pd.DataFrame(sequences)
        sequences_df.index.name = "timeindex"
        sequences_df.index = building.timeindex(year=str(scenario_year))

    sequences_cop = pd.concat([gshp_cop, ashp_cop], axis=1)
    sequences_cop.columns = ["DE-gshp-profile", "DE-ashp-profile"]
    sequences_cop.index.name = "timeindex"
    sequences_cop.index = building.timeindex(year=str(scenario_year))

    building.write_sequences(
        "efficiency_profile.csv",
        sequences_cop,
        directory=os.path.join(datapackage_dir, "data/sequences"),
    )

    if "NEPC" in scenario:

        must_run_sequences = {}

        must_run_sequences["DE-must-run-profile"] = (
            df.loc[weather_year][b + "_heat_demand_total"]
            / df.loc[weather_year][b + "_heat_demand_total"].max()
        )

        must_run_sequences_df = pd.DataFrame(must_run_sequences)
        must_run_sequences_df = (must_run_sequences_df * 3 * 8300).clip(
            upper=8300
        ) / 8300  # calibrate for 2030NEPC
        must_run_sequences_df.index.name = "timeindex"
        must_run_sequences_df.index = building.timeindex(
            year=str(scenario_year)
        )

        building.write_sequences(
            "volatile_profile.csv",
            must_run_sequences_df,
            directory=os.path.join(datapackage_dir, "data/sequences"),
        )

    building.write_elements(
        "heat_load.csv",
        pd.DataFrame([i for i in elements if i["type"] == "load"]).set_index(
            "name"
        ),
        directory=os.path.join(datapackage_dir, "data/elements"),
    )

    building.write_elements(
        "heatpump.csv",
        pd.DataFrame(
            [i for i in elements if i["type"] == "conversion"]
        ).set_index("name"),
        directory=os.path.join(datapackage_dir, "data/elements"),
    )

    building.write_elements(
        "heat_storage.csv",
        pd.DataFrame(
            [i for i in elements if i["type"] == "storage"]
        ).set_index("name"),
        directory=os.path.join(datapackage_dir, "data/elements"),
    )

    building.write_elements(
        "bus.csv",
        el_buses,
        directory=os.path.join(datapackage_dir, "data/elements"),
        replace=True,
    )

    building.write_sequences(
        "heat_load_profile.csv",
        sequences_df,
        directory=os.path.join(datapackage_dir, "data/sequences"),
    )
