import os

from datapackage import Package

import pandas as pd

import json
import matplotlib.pyplot as plt
from oemof.tools.economics import annuity

path = os.path.join(os.getcwd(), "results")

scenario_year = 2050
wacc = 0.05

technologies = pd.DataFrame(
    Package(
        "https://raw.githubusercontent.com/ZNES-datapackages/"
        "angus-input-data/master/technology/datapackage.json"
    )
    .get_resource("technology")
    .read(keyed=True)
).set_index(["year", "parameter", "carrier", "tech"])

heat = pd.DataFrame(
    Package(
        "https://raw.githubusercontent.com/ZNES-datapackages/"
        "angus-input-data/master/technology/datapackage.json"
    )
    .get_resource("heat")
    .read(keyed=True)
).set_index(["year", "parameter", "carrier", "tech"])


technologies = pd.concat([technologies, heat])

ct = [
    ("hydrogen", "storage"),
    ("lithium", "battery"),
    ("decentral_heat", "tes"),
]


capacity_cost = {}
storage_capacity_cost = {}

for carrier, tech in ct:
    capacity_cost[carrier, tech] = (
        annuity(
            float(
                technologies.loc[
                    (scenario_year, "capex_power", carrier, tech), "value"
                ]
            ),
            float(
                technologies.loc[
                    (scenario_year, "lifetime", carrier, tech), "value"
                ]
            ),
            wacc,
        )
        * 1000,  # €/kW -> €/MW
    )[0]

    storage_capacity_cost[carrier, tech] = (
        annuity(
            float(
                technologies.loc[
                    (scenario_year, "capex_energy", carrier, tech), "value"
                ]
            ),
            float(
                technologies.loc[
                    (scenario_year, "lifetime", carrier, tech), "value"
                ]
            ),
            wacc,
        )
        * 1000,  # €/kWh -> €/MWh
    )[0]


tes_storage_capacity = {}
tes_capacity = {}
tescost = {}
for dir in os.listdir(path):
    if not "flex" in dir:
        tes_storage_capacity[dir] = (
            pd.read_csv(
                os.path.join(path, dir, "output", "filling_levels.csv"),
                index_col=0,
                parse_dates=True,
            )["DE-flex-decentral_heat-tes"].max()
            * storage_capacity_cost["decentral_heat", "tes"]
        )

        capacity = pd.read_csv(
            os.path.join(path, dir, "output", "capacities.csv"),
            index_col=[0, 1, 2, 3, 4],
        )

        tes_capacity[dir] = (
            capacity.loc[
                (
                    "DE-flex-decentral_heat-tes",
                    "DE-flex-decentral_heat-bus",
                    "invest",
                    "tes",
                    "decentral_heat",
                ),
                "value",
            ]
            * capacity_cost["decentral_heat", "tes"]
        )

        tescost[dir] = tes_capacity[dir] + tes_storage_capacity[dir]
tescost = pd.Series(tescost)

elstorage = {}
for dir in os.listdir(path):
    capacity = pd.read_csv(
        os.path.join(path, dir, "output", "capacities.csv"),
        index_col=[0, 1, 2, 3, 4],
    )

    for bus in ["DE"]:
        hydstor = capacity.loc[
            (
                bus + "-hydrogen-storage",
                bus + "-electricity",
                "invest",
                "storage",
                "hydrogen",
            ),
            "value",
        ]

        hydstor = (
            hydstor * 168 * storage_capacity_cost["hydrogen", "storage"]
            + hydstor * capacity_cost["hydrogen", "storage"]
        )

        lithstor = capacity.loc[
            (
                bus + "-lithium-battery",
                bus + "-electricity",
                "invest",
                "battery",
                "lithium",
            ),
            "value",
        ]

        lithstor = (
            lithstor * 6.5 * storage_capacity_cost["lithium", "battery"]
            + lithstor * capacity_cost["lithium", "battery"]
        )

        elstorage[(bus, dir)] = (lithstor, hydstor)

obj = {}
for dir in os.listdir(path):
    with open(os.path.join(path, dir, "modelstats.json")) as json_data:
        data = json.load(json_data)
        obj[dir] = data["problem"]["Lower bound"]

obj = pd.Series(obj)
flex0 = obj[[c for c in obj.index if "flex" in c]]
flex100 = obj[[c for c in obj.index if not "flex" in c]]
flex0.index = [c.replace("-flex0", "") for c in flex0.index]

final = pd.concat(
    [flex0 / 1e9, flex100 / 1e9, ((flex0 - flex100) / flex0) * 100],
    axis=1,
    sort=False,
)
base_scenarios = ["2050REF", "2040DG", "2040GCA", "2030DG"]
final.columns = ["No-Flex in (in bn Euro)", "Flex (in bn Euro)", "Change in %"]
final.loc[base_scenarios].round(2).to_latex(
    "documentation/tables/investment_cost.tex"
)  # plot(kind="bar", cmap=plt.get_cmap("coolwarm"))
