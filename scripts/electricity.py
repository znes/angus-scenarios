# -*- coding: utf-8 -*-
"""
"""
import json
import os

from datapackage import Package

import pandas as pd


from oemof.tabular.datapackage import building


def tyndp_generation_2018(
    countries, vision, scenario, scenario_year, datapackage_dir, raw_data_path,
    ccgt_share=0.5
):
    """Extracts TYNDP2018 generation data and writes to datapackage for oemof
    tabular usage

    Parameters
    -----------
    countries: list
        List with countries to extract (Names in country codes)
    vision: str
        TYNDP Vision (one of 2040 GCA, 2030 DG, etc.)
    scenario: str
        Name of scenario to be used for cost assumptions etc
    scenario_year: str
        Year of scenario
    datapackage_dir: string
        Directory for tabular resource
    raw_data_path: string
        Path where raw data file
        `ENTSO%20Scenario%202018%20Generation%20Capacities.xlsm` is located
    ccgt_share:
        Share of ccgt generation of total gas generation
    """

    filepath = building.download_data(
        "https://www.entsoe.eu/Documents/TYNDP%20documents/TYNDP2018/"
        "Scenarios%20Data%20Sets/ENTSO%20Scenario%202018%20Generation%20Capacities.xlsm",
        directory=raw_data_path,
    )
    df = pd.read_excel(
        filepath, sheet_name=vision, index_col=0, skiprows=[0, 1]
    )

    colnames = [
        "Biofuels",
        "Gas",
        "Hard coal",
        "Hydro-pump",
        "Hydro-run",
        "Hydro-turbine",
        "Lignite",
        "Nuclear",
        "Oil",
        "Othernon-RES",
        "Other RES",
        "Solar-thermal",
        "Solar-\nPV",
        "Wind-\non-shore",
        "Wind-\noff-shore",
    ]

    newnames = [
        ("biomass", "st"),
        ("gas", "ocgt"),
        ("coal", "st"),
        ("hydro", "phs"),
        ("hydro", "ror"),
        ("hydro", "rsv"),
        ("lignite", "st"),
        ("uranium", "st"),
        ("oil", "ocgt"),
        ("mixed", "st"),
        ("other", "res"),
        ("solar", "thermal"),
        ("solar", "pv"),
        ("wind", "onshore"),
        ("wind","offshore"),
    ]

    df = df.rename(columns=dict(zip(colnames, newnames)))
    df[("biomass", "st")] += df[("other", "res")]
    df.drop([("other", "res")], axis=1, inplace=True)
    df.index.name = "zones"
    df.reset_index(inplace=True)
    df = pd.concat(
        [
            pd.DataFrame(
                df["zones"].apply(lambda row: [row[0:2], row[2::]]).tolist(),
                columns=["country", "zone"],
            ),
            df,
        ],
        axis=1,
    )

    df = df.groupby("country").sum()

    df[("gas", "ccgt")] = df[("gas", "ocgt")] * ccgt_share
    df[("gas", "ocgt")] = df[("gas", "ocgt")] * (1 - ccgt_share)

    # as raw data is divided in turbine and pump (where turbine is also from
    # pump storages as well as reservoirs)
    df[("hydro", "rsv")] = (df[("hydro", "rsv")] - df[("hydro", "phs")]).clip(0)


    technologies = pd.DataFrame(
        # Package('/home/planet/data/datapackages/technology-cost/datapackage.json')
        Package(
            "https://raw.githubusercontent.com/ZNES-datapackages/"
            "angus-input-data/master/technology/datapackage.json"
        )
        .get_resource("technology")
        .read(keyed=True)
    ).set_index(["year", "parameter", "carrier", "tech"])

    carrier_package = Package(
        "https://raw.githubusercontent.com/ZNES-datapackages/"
        "angus-input-data/master/carrier/datapackage.json"
    )

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

    elements = _elements(
        countries, df, technologies, carrier_cost, emission_factors,
        scenario, scenario_year)

    df = pd.DataFrame.from_dict(elements, orient="index")
    df = df[df.capacity != 0]

    # write elements to CSV-files
    for element_type in ["dispatchable", "volatile", "conversion"]:
        building.write_elements(
            element_type + ".csv",
            df.loc[df["type"] == element_type].dropna(how="all", axis=1),
            directory=os.path.join(datapackage_dir, "data", "elements"),
        )


def german_energy_system(
    datapackage_dir,
    raw_data_path,
    scenario_name,
    cost_scenario,
    technologies,
    scenario_year,
):
    """Extracts german specific scenario data from input datapackage

    Parameters
    -----------
    scenario_name: str
        Name of scenario
    scenario_year: int
        Year of scenario (one of 2030, 2040, 2050)
    cost_scenario: str
        Name of cost scenario
    technologies: DataFrame
        DataFrame with the technology data like efficiencies etc.
    datapackage_dir: string
        Directory for tabular resource
    raw_data_path: string
        Path where raw data file is located
    """

    data = (
        pd.DataFrame(
            Package(
                "https://raw.githubusercontent.com/ZNES-datapackages/"
                "angus-input-data/master/capacities/datapackage.json"
            )
            .get_resource("german-electricity-system")
            .read(keyed=True)
        )
        .set_index(["scenario", "year", "carrier", "tech"])
        .loc[(scenario_name, scenario_year)]
    )

    carrier_package = Package(
        "https://raw.githubusercontent.com/ZNES-datapackages/"
        "angus-input-data/master/carrier/datapackage.json"
    )

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

    elements = {}

    # prepare data for usage in _elements() function
    countries = ["DE"]
    _data = data["value"].T
    _data.name = "DE"
    _data = _data.to_frame().T

    elements = _elements(
        countries, _data, technologies, carrier_cost, emission_factors,
        cost_scenario, scenario_year)

    df = pd.DataFrame.from_dict(elements, orient="index")

    for element_type in [
        "dispatchable",
        "volatile",
        "conversion",
        "storage",
        "load",
    ]:

        building.write_elements(
            element_type + ".csv",
            df.loc[df["type"] == element_type].dropna(how="all", axis=1),
            directory=os.path.join(datapackage_dir, "data", "elements"),
            overwrite=True,
        )


def ehighway_generation(
    countries,
    cost_scenario,
    scenario="100% RES",
    datapackage_dir=None,
    raw_data_path=None,
    ccgt_share=0.5,
    scenario_year=2050
):
    """
    """
    scenario_mapper = {"100% RES": "T54"}

    filename = "e-Highway_database_per_country-08022016.xlsx"

    data = pd.read_excel(
        building.download_data(
            "http://www.e-highway2050.eu/fileadmin/documents/Results/"
            + filename,
            directory=raw_data_path,
        ),
        sheet_name=scenario_mapper[scenario],
        index_col=[1],
        skiprows=3,
        encoding="utf-8",
    )
    data = data.loc[countries]

    technologies = pd.DataFrame(
        # Package('/home/planet/data/datapackages/technology-cost/datapackage.json')
        Package(
            "https://raw.githubusercontent.com/ZNES-datapackages/"
            "angus-input-data/master/technology/datapackage.json"
        )
        .get_resource("technology")
        .read(keyed=True)
    ).set_index(["year", "parameter", "carrier", "tech"])

    carrier_package = Package(
        "https://raw.githubusercontent.com/ZNES-datapackages/"
        "angus-input-data/master/carrier/datapackage.json"
    )

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
    data["CCGT"] = data["TOTAL GAS"] * ccgt_share
    data["OCGT"] = data["TOTAL GAS"] * (1 - ccgt_share)

    rename_cols = {
        "Wind": ("wind", "onshore"),
        "Wind         North Sea": ("wind", "offshore"),
        "PV": ("solar", "pv"),
        "OCGT": ("gas", "ocgt"),
        "CCGT": ("gas", "ccgt"),
        "Biomass I": ("biomass", "st"), # use only regional biomass potential
        "RoR": ("hydro", "ror"),
        "PSP": ("hydro", "phs"),
        "Hydro with reservoir": ("hydro", "rsv"),
    }
    data.rename(columns=rename_cols, inplace=True)

    data = data[[i for i in rename_cols.values()]]

    elements = _elements(
        countries, data, technologies, carrier_cost, emission_factors,
        cost_scenario, scenario_year)

    df = pd.DataFrame.from_dict(elements, orient="index")
    df = df[df.capacity != 0]

    for element_type in [
        "dispatchable",
        "volatile",
        "conversion",
        "storage",
        "reservoir",
        "load",
    ]:
        building.write_elements(
            element_type + ".csv",
            df.loc[df["type"] == element_type].dropna(how="all", axis=1),
            directory=os.path.join(datapackage_dir, "data", "elements"),
            overwrite=True,
        )


def excess(datapackage_dir):
    """
    """
    path = os.path.join(datapackage_dir, "data", "elements")
    buses = building.read_elements("bus.csv", directory=path)

    buses.index.name = "bus"
    buses = buses.loc[buses["carrier"] == "electricity"]

    elements = pd.DataFrame(buses.index)
    elements["type"] = "excess"
    elements["carrier"] = "electricity"
    elements["tech"] = "excess"
    elements["name"] = elements["bus"] + "-excess"
    elements["marginal_cost"] = 0

    elements.set_index("name", inplace=True)

    building.write_elements("excess.csv", elements, directory=path)


def shortage(datapackage_dir):
    """
    """
    path = os.path.join(datapackage_dir, "data", "elements")
    buses = building.read_elements("bus.csv", directory=path)

    buses = buses.loc[buses["carrier"] == "electricity"]
    buses.index.name = "bus"

    elements = pd.DataFrame(buses.index)
    elements["capacity"] = 10e10
    elements["type"] = "shortage"
    elements["carrier"] = "electricity"
    elements["tech"] = "shortage"
    elements["name"] = elements["bus"] + "-shortage"
    elements["marginal_cost"] = 3000

    elements.set_index("name", inplace=True)

    building.write_elements("shortage.csv", elements, directory=path)



def _elements(countries, data, technologies, carrier_cost, emission_factors,
               scenario, scenario_year):
    elements = {}
    for b in countries:
        for carrier, tech in data.columns:

            element = {}
            elements["-".join([b, carrier, tech])] = element

            if tech in ["onshore", "offshore", "pv"]:

                profile = "-".join([b, tech, "profile"])
                element.update({
                    "bus": b + "-electricity",
                    "tech": tech,
                    "carrier": carrier,
                    "capacity": data.at[b, (carrier, tech)],
                    "type": "volatile",
                    "profile": profile,
                    "output_parameters": json.dumps({}),
                })

            elif carrier in [
                "gas",
                "coal",
                "lignite",
                "oil",
                "uranium",
                "mixed",
            ]:
                marginal_cost = float(
                    carrier_cost.at[(scenario, carrier), "value"]
                    + emission_factors.at[carrier, "value"]
                    * carrier_cost.at[(scenario, "co2"), "value"]
                ) / float(
                    technologies.loc[
                        (scenario_year, "efficiency", carrier, tech), "value"
                    ]
                ) + float(
                    technologies.loc[(2050, "vom", carrier, tech), "value"]
                )

                emission_factor = float(
                    emission_factors.at[carrier, "value"] /
                    technologies.loc[
                        (scenario_year, "efficiency", carrier, tech), "value"]
                )

                element.update(
                    {
                        "carrier": carrier,
                        "carrier_cost": carrier_cost.at[
                            (scenario, carrier), "value"
                        ],
                        "efficiency": float(
                            technologies.loc[
                                (scenario_year, "efficiency", carrier, tech),
                                "value",
                            ]
                        ),
                        "capacity": data.at[b, (carrier, tech)],
                        "bus": b + "-electricity",
                        "type": "dispatchable",
                        "marginal_cost": marginal_cost,
                        "profile": technologies.loc[
                            (2050, "avf", carrier, tech), "value"
                        ],
                        "tech": tech,
                        "output_parameters": json.dumps({
                            "emission_factor": emission_factor}
                        )
                    }
                )

            elif carrier == "biomass":
                element.update(
                    {
                        "carrier": carrier,
                        "capacity": data.at[b, (carrier, tech)],
                        "to_bus": b + "-electricity",
                        "efficiency": technologies.loc[
                            (scenario_year, "efficiency", carrier, "st"),
                            "value",
                        ],
                        "from_bus": b + "-biomass-bus",
                        "type": "conversion",
                        "output_parameters": json.dumps({}),
                        "carrier_cost": float(
                            carrier_cost.at[(scenario, carrier), "value"]
                        ),
                        "tech": tech,
                    }
                )

            elif tech in ["battery", "caes"]:
                elements["-".join([b, carrier, tech])] = element
                element.update(
                    {
                        "storage_capacity": float(
                            float(technologies.loc[
                                (scenario_year,
                                 "storage_capacity",
                                 carrier,
                                 tech),
                                "value",
                            ])
                            * float(data.at[b, (carrier, tech)])
                        ),
                        "capacity": float(data.at[b, (carrier, tech)]),
                        "bus": b + "-electricity",
                        "tech": tech,
                        "carrier": carrier,
                        "type": "storage",
                        "efficiency": float(
                            technologies.loc[
                                (scenario_year, "efficiency", carrier, tech),
                                "value",
                            ])
                        ** 0.5,  # convert roundtrip to input / output efficiency
                        "marginal_cost": 0,
                        "loss": 0,
                    }
                )

            elif "load" in tech:
                # remove once heat components are merged
                if carrier != "heat":
                    elements["-".join([b, carrier, tech])] = element
                    element.update(
                        {
                            "amount": data.at[b, (carrier, tech)] * 1000,
                            "bus": b + "-electricity",
                            "tech": tech,
                            "carrier": carrier,
                            "type": "load",
                            "profile": "-".join([b, carrier, tech, "profile"]),
                        }
                    )
    return elements
