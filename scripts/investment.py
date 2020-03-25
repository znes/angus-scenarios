# -*- coding: utf-8 -*-
"""
"""
import json
import os

from datapackage import Package
import pandas as pd

from oemof.tabular.datapackage import building
from oemof.tools.economics import annuity

def storage(
    datapackage_dir,
    raw_data_path,
    cost_scenario,
    countries,
    technologies,
    scenario_year,
    wacc
):
    """Extracts german specific scenario data from input datapackage

    Parameters
    -----------
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


    # carrier_package = Package(
    #     "https://raw.githubusercontent.com/ZNES-datapackages/"
    #     "angus-input-data/master/carrier/datapackage.json"
    # )

    # carrier_cost = (
    #     pd.DataFrame(
    #         carrier_package.get_resource("carrier-cost").read(keyed=True)
    #     )
    #     .set_index(["scenario", "carrier"])
    #     .sort_index()
    # )
    #
    # emission_factors = (
    #     pd.DataFrame(
    #         carrier_package.get_resource("emission-factor").read(keyed=True)
    #     )
    #     .set_index(["carrier"])
    #     .sort_index()
    # )

    potential = (
        Package(
            "https://raw.githubusercontent.com/ZNES-datapackages/"
            "technology-potential/master/datapackage.json"
        )
        .get_resource("renewable")
        .read(keyed=True)
    )
    potential = pd.DataFrame(potential).set_index(["country", "tech"])
    potential = potential.loc[
        potential["source"] == "Brown & Schlachtberger"
    ]

    elements = {}
    storages = [
        ("lithium", "battery"), ("hydrogen", "storage")]
    for b in countries:
        for carrier, tech in storages:

            element = {}
            elements["-".join([b, carrier, tech])] = element
            # if tech not in storages:
            #     capacity_cost = (
            #         float(technologies.loc[(scenario_year, "fom", carrier, tech), "value"]) +
            #         annuity(
            #             float(technologies.loc[
            #                 (scenario_year, "capex", carrier, tech), "value"]),
            #             float(technologies.loc[
            #                 (scenario_year, "lifetime", carrier, tech), "value"]),
            #             wacc
            #             ) * 1000,  # €/kW -> €/M
            #     )[0]
            # else:
            capacity_cost = (
                annuity(
                    float(technologies.loc[
                        (scenario_year, "capex_power", carrier, tech), "value"]),
                    float(technologies.loc[
                        (scenario_year, "lifetime", carrier, tech), "value"]),
                    wacc
                    ) * 1000,  # €/kW -> €/MW
            )[0]

            storage_capacity_cost = (
                float(technologies.loc[(scenario_year, "fom", carrier, tech), "value"]) +
                annuity(
                    float(technologies.loc[
                        (scenario_year, "capex_energy", carrier, tech), "value"]),
                    float(technologies.loc[
                        (scenario_year, "lifetime", carrier, tech), "value"]),
                    wacc
                    ) * 1000,  # €/kWh -> €/MWh
            )[0]
            #
            # if tech in ["onshore", "offshore", "pv"]:
            #
            #     potential_mapper = {
            #         "onshore": "wind_onshore", "offshore": "wind_offshore", "pv": "pv"}
            #     if tech == "offshore" and b in ["CH", "CZ", "AT", "LU"]:
            #         pass
            #     else:
            #         profile = "-".join([b, tech, "profile"])
            #         element.update({
            #             "bus": b + "-electricity",
            #             "tech": tech,
            #             "carrier": carrier,
            #             "capacity_potential": float(
            #                 potential.loc[(b, potential_mapper[tech]),
            #                               "capacity_potential"]),
            #             "capacity": 0,
            #             "expandable": True,
            #             "capacity_cost": capacity_cost,
            #             "type": "volatile",
            #             "profile": profile,
            #             "output_parameters": json.dumps({}),
            #         })
            #
            # elif carrier in [
            #     "gas",
            #     "coal",
            #     "lignite",
            #     "oil",
            #     "uranium",
            #     "mixed",
            # ]:
            #     marginal_cost = float(
            #         carrier_cost.at[(cost_scenario, carrier), "value"]
            #         + emission_factors.at[carrier, "value"]
            #         * carrier_cost.at[(cost_scenario, "co2"), "value"]
            #     ) / float(
            #         technologies.loc[
            #             (scenario_year, "efficiency", carrier, tech), "value"
            #         ]
            #     ) + float(
            #         technologies.loc[(2050, "vom", carrier, tech), "value"]
            #     )
            #
            #     emission_factor = float(
            #         emission_factors.at[carrier, "value"] /
            #         technologies.loc[
            #             (scenario_year, "efficiency", carrier, tech), "value"]
            #     )
            #
            #     element.update(
            #         {
            #             "carrier": carrier,
            #             "carrier_cost": float(carrier_cost.at[
            #                 (cost_scenario, carrier), "value"
            #             ]),
            #             "efficiency": float(
            #                 technologies.loc[
            #                     (scenario_year, "efficiency", carrier, tech),
            #                     "value",
            #                 ]
            #             ),
            #             "capacity": 0,
            #             "expandable": True,
            #             "capacity_cost": capacity_cost,
            #             "bus": b + "-electricity",
            #             "type": "dispatchable",
            #             "marginal_cost": marginal_cost,
            #             "profile": technologies.loc[
            #                 (2050, "avf", carrier, tech), "value"
            #             ],
            #             "tech": tech,
            #             "output_parameters": json.dumps({
            #                 "emission_factor": emission_factor}
            #             )
            #         }
            #     )
            #
            # elif carrier == "biomass":
            #     element.update(
            #         {
            #             "carrier": carrier,
            #             "capacity": 0,
            #             "to_bus": b + "-electricity",
            #             "efficiency": technologies.loc[
            #                 (scenario_year, "efficiency", carrier, "st"),
            #                 "value",
            #             ],
            #             "expandable": True,
            #             "capacity_cost": capacity_cost,
            #             "from_bus": b + "-biomass-bus",
            #             "type": "conversion",
            #             "output_parameters": json.dumps({}),
            #             "carrier_cost": float(
            #                 carrier_cost.at[(cost_scenario, carrier), "value"]
            #             ),
            #             "tech": tech,
            #         }
            #     )

            if (carrier, tech) in storages:
                elements["-".join([b, carrier, tech])] = element
                element.update(
                    {

                        "invest_relation_input_capacity": 1 / float(technologies.loc[
                                (scenario_year, "max_hours", carrier, tech),
                                "value",
                            ]),
                        "invest_relation_output_capacity": 1 / float(technologies.loc[
                                (scenario_year, "max_hours", carrier, tech),
                                "value",
                            ]),
                        "capacity": 0,
                        "storage_capacity": 0,
                        "bus": b + "-electricity",
                        "expandable": True,
                        "capacity_cost": capacity_cost,
                        "storage_capacity_cost": storage_capacity_cost,
                        "tech": tech,
                        "marginal_cost": 1,
                        "carrier": carrier,
                        "type": "storage",
                        "efficiency": float(
                            technologies.loc[
                                (scenario_year, "efficiency", carrier, tech),
                                "value",
                            ])
                        ** 0.5,  # convert roundtrip to input / output efficiency
                        "loss": 0,
                    }
                )



    df = pd.DataFrame.from_dict(elements, orient="index")
    for element_type in [
        # "dispatchable",
        # "volatile",
        # "conversion",
        "storage"
    ]:

        building.write_elements(
            element_type + ".csv",
            df.loc[df["type"] == element_type].dropna(how="all", axis=1),
            directory=os.path.join(datapackage_dir, "data", "elements"),
            replace=False,
            overwrite=True,
        )


def _load(countries, data, sensitivities=None):

    if sensitivities is not None:
        for k,v in sensitivities.items():
            k = k.split("-")
            data.at[k[0], (k[1], k[2])] = v

    elements = {}
    for b in countries:
        for carrier, tech in data.columns:
            element = {}
            elements["-".join([b, carrier, tech])] = element

            if "load" in tech:
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
