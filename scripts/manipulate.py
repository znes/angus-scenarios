import os

from datapackage import Package
import pandas as pd

from oemof.tabular.datapackage import building


def storage(scenario_name, scenario_year, datapackage_dir, raw_data_path):
    """
    """
    dir = os.path.join(datapackage_dir, "data", "elements")

    technologies = pd.DataFrame(
        Package(
            "https://raw.githubusercontent.com/ZNES-datapackages/"
            "angus-input-data/master/technology/datapackage.json"
        )
        .get_resource("technology")
        .read(keyed=True)
    ).set_index(["year", "parameter", "carrier", "tech"])

    data = pd.DataFrame(
        Package(
            "https://raw.githubusercontent.com/ZNES-datapackages/"
            "angus-input-data/master/capacities/datapackage.json"
        )
        .get_resource("storage")
        .read(keyed=True)
    ).set_index(["scenario"])

    storage = building.read_elements("storage.csv", dir)

    elements = {}
    for c in data.columns:
        elements["DE-" + c] = {
            "storage_capacity": technologies.loc[
                (
                    scenario_year,
                    "storage_capacity",
                    c.split("-")[0],
                    c.split("-")[1],
                ),
                "value",
            ]
            * data.at[scenario_name, c],
            "capacity": data.at[scenario_name, c],
            "bus": "DE-electricity",
            "tech": "caes",
            "carrier": "air",
            "type": "storage",
            "efficiency": float(
                technologies.loc[
                    (
                        scenario_year,
                        "efficiency",
                        c.split("-")[0],
                        c.split("-")[1],
                    ),
                    "value",
                ]
            )
            ** 0.5,  # convert roundtrip to input / output efficiency
            "marginal_cost": 0,
            "loss": 0,
        }

    for k in elements:
        if k in storage.index:
            storage.drop(k, inplace=True)
    storage = pd.concat([storage, pd.DataFrame(elements).T])
    # write each 'row' to replace existing data...
    building.write_elements(
        "storage.csv", storage, directory=dir,
        replace=True
    )



#
# p = Package("../angus-input-data/capacities/datapackage.json")
# p.get_resource('storage ').read(keyed=True)
