import os
import pandas as pd
import matplotlib.pyplot as plt
import datapackage as dp
import plotly.io as pio
import plotly.offline as offline
from datapackage import Package
from tabulate import tabulate
from oemof.tabular.datapackage import building
from matplotlib import colors
%matplotlib inline

color = {
    "caes": "brown",
    "air-caes": "brown",
    "gas-ocgt": "gray",
    "gas-ccgt": "lightgray",
    "solar-pv": "gold",
    "wind-onshore": "skyblue",
    "wind-offshore": "darkblue",
    "biomass-ce": "olivedrab",
    "battery": "lightsalmon",
    "electricity": "lightsalmon",
    "hydro-ror": "aqua",
    "hydro-phs": "darkred",
    "hydro-reservoir": "magenta",
    "biomass": "olivedrab",
    "uranium": "yellow",
    "hydro": "aqua",
    "wind": "skyblue",
    "solar": "gold",
    "gas": "lightgray",
    "lignite": "chocolate",
    "coal": "dimgrey",
    "waste": "yellowgreen",
    "oil": "black",
    "import": "pink",
    "storage": "green",
    "other": "red",
    "mixed": "saddlebrown",
    "mixed-gt": "darkcyan",
    "mixed-chp": "saddlebrown",
    "chp": "red",
    "NONE": "blue",
}

color_dict = {name: colors.to_hex(color) for name, color in color.items()}

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

# carrier cost
print(tabulate(carrier_cost.reset_index().set_index("scenario"), tablefmt="pipe", headers="keys"))

# technology assumptions
df = technologies.unstack([2,3]).loc[(slice(None), "efficiency"),"value"].T.reset_index().set_index("carrier")

df.columns = ["tech", "2030", "2040", "2050"]
print(tabulate(df.fillna("NA"), tablefmt="pipe", headers="keys"))

# installed capacities
conv = building.read_elements(
    "/home/admin/projects/angus-scenarios/"
    "datapackages/2040GCA/data/elements/dispatchable.csv")

renew = building.read_elements(
    "/home/admin/projects/angus-scenarios/"
    "datapackages/2040GCA/data/elements/volatile.csv")

all = pd.concat([conv, renew], sort=True)
all.reset_index(inplace=True)
all["name"] = ["-".join(i.split("-")[1:]) for i in all["name"]]
all.set_index(["name", "bus"], inplace=True)
all = all.groupby(["bus","carrier"]).sum()["capacity"].unstack().fillna(0)
all.index = [i.split("-")[0] for i in all.index]



ax = (all/1000).plot(kind='bar', stacked=True, color=[color_dict.get(c) for c in all.columns])
plt.xticks(rotation=45)
plt.savefig("documentation/installed_capacities.pdf")

print(tabulate(all, tablefmt="pipe", headers="keys"))
