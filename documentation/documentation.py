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
import seaborn
%matplotlib inline

color = {
    "caes": "brown",
    "conventional": "dimgrey",
    "air-caes": "brown",
    "gas-ocgt": "gray",
    "gas-ccgt": "lightgray",
    "solar-pv": "gold",
    "pv": "gold",
    "wind-onshore": "skyblue",
    "onshore": "skyblue",
    "wind-offshore": "darkblue",
    "offshore": "darkblue",
    "biomass-st": "olivedrab",
    "biomass": "olivedrab",
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
    "coal-st": "dimgrey",
    "waste": "yellowgreen",
    "oil-ocgt": "black",
    "import": "pink",
    "storage": "green",
    "other": "red",
    "other-res": "darkred",
    "mixed": "saddlebrown",
    "mixed-gt": "darkcyan",
    "mixed-chp": "saddlebrown",
    "chp": "red",
    "NONE": "blue",
}

color_dict = {name: colors.to_hex(color) for name, color in color.items()}

#########################
technologies = pd.DataFrame(
    # Package('/home/planet/data/datapackages/technology-cost/datapackage.json')
    Package(
        "https://raw.githubusercontent.com/ZNES-datapackages/"
        "angus-input-data/master/technology/datapackage.json"
    )
    .get_resource("technology")
    .read(keyed=True)
).set_index(["year", "parameter", "carrier", "tech"])

# eta assumptions
eta = technologies.unstack([2,3]).loc[(slice(None), "efficiency"),"value"].T.reset_index().set_index("carrier")
eta.columns = ["tech", "2030", "2040", "2050"]
print(tabulate(eta.fillna("NA"), tablefmt="pipe", headers="keys"))


## all parameters
print(tabulate(technologies.reset_index().set_index('year').sort_index().fillna("NA"), tablefmt="pipe", headers="keys"))


# carrier cost
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

print(tabulate(carrier_cost.reset_index().set_index("scenario"), tablefmt="pipe", headers="keys"))


# carrier cost
hydro_data = Package(
    "https://raw.githubusercontent.com/ZNES-datapackages/"
    "angus-input-data/master/hydro/datapackage.json"
)

hydro = pd.DataFrame(
        hydro_data.get_resource("hydro").read(keyed=True)
    ).set_index(["country", "year"]).sort_index()
print(tabulate(hydro.reset_index().drop("source", axis=1).set_index("country"), tablefmt="pipe", headers="keys"))


# installed capacities
path = os.path.join(os.getcwd(), "datapackages")
df = pd.DataFrame()
load = pd.DataFrame()
storage = pd.DataFrame()

for dir in os.listdir(path):
    storage = pd.read_csv(os.path.join(
            path, dir, "data/elements/storage.csv"), sep=";", index_col=0
        )
    phs = pd.read_csv(os.path.join(
            path, dir, "data/elements/phs.csv"), sep=";", index_col=0
        )
    conv = pd.read_csv(os.path.join(
            path, dir, "data/elements/dispatchable.csv"), sep=";", index_col=0
        )

    renew = pd.read_csv(os.path.join(
            path,  dir, "data/elements/volatile.csv"), sep=";", index_col=0
        )
    conversion = pd.read_csv(os.path.join(
            path,  dir, "data/elements/conversion.csv"), sep=";", index_col=0
        )
    conversion.rename(columns={"to_bus": "bus"}, inplace=True)

    _load = pd.read_csv(os.path.join(
            path,  dir, "data/elements/load.csv"), sep=";", index_col=0
        )
    _load["scenario"] = dir
    load = pd.concat([load, _load], sort=True)


    capacities = pd.concat([conv, renew, conversion, phs, storage], sort=True)
    capacities["scenario"] = dir
    df = pd.concat([df, capacities], sort=True)

df["name"] = ["-".join(i.split("-")[1:]) for i in df.index]
df = df.set_index(["name", "bus", "scenario"])["capacity"]

df_GW = df/1e3
df_GW = (df_GW.unstack(1).reset_index().set_index("scenario")).round(1).replace(0, "-").sort_index().fillna("-")
df_GW.columns = [i.split("-")[0] for i in df_GW.columns]

print(tabulate(df_GW, tablefmt="pipe", headers="keys"))


# German capacities
de = df.loc[(slice(None), "DE-electricity")].unstack(0).fillna(0).T.round(0)
print(tabulate(de.sort_index(), tablefmt="pipe", headers="keys"))

de = de / 1000
ax = (de.T).plot(kind='bar', stacked=True, color=[color_dict.get(c) for c in de.index])
lgd = ax.legend(loc='upper left', bbox_to_anchor=(1, 1), shadow=True, ncol=1)
ax.set_ylabel("Installed capacity in GW")
plt.xticks(rotation=45)
#plt.plot(figsize=(10, 5))
plt.savefig("documentation/installed_capacities.pdf", bbox_extra_artists=(lgd,), bbox_inches='tight')


# FLH renewables
volatile_profile = pd.read_csv(os.path.join(
        path, "ZNES2050", "data/sequences/volatile_profile.csv"), sep=";", index_col=0
    ).sum()

ror_profile = pd.read_csv(os.path.join(
        path, "ZNES2050", "data/sequences/ror_profile.csv"), sep=";", index_col=0
    ).sum()
ror_profile.index = [i.split("-")[0] for i in ror_profile.index]

volatile_profile = volatile_profile.to_frame()
volatile_profile["country"] = [i.split("-")[0] for i in volatile_profile.index]
volatile_profile["tech"] = [i.split("-")[1] for i in volatile_profile.index]
volatile_flh = volatile_profile.set_index(["country", "tech"]).unstack("tech").droplevel(0, axis=1)
volatile_flh["ror"] = ror_profile
print(tabulate((volatile_flh.round(0)), tablefmt="pipe", headers="keys"))


# Biomass potential
biomass = pd.read_csv(os.path.join(
        path, "ZNES2050", "data/elements/commodity.csv"), sep=";", index_col=0
    )
biomass = biomass["amount"] / 1e6
biomass.index = [i.split("-")[0] for i in biomass.index]
print(tabulate((biomass.to_frame()), tablefmt="pipe", headers="keys"))

load["name"] = ["-".join(i.split("-")[1:]) for i in load.index]
load = load.set_index(["name", "bus", "scenario"])["amount"]
load.index = load.index.droplevel(0)
print(tabulate((load.unstack(1)/1e6).round(2), tablefmt="pipe", headers="keys"))


## all countries
for dir in os.listdir("datapackages"):
    scenario = df.loc[(slice(None), slice(None), dir)].unstack().fillna(0).round(0)
    scenario.columns = [c[0:2] for c in scenario.columns]
    print(tabulate(scenario.T, tablefmt="pipe", headers="keys"))

#
# path = os.path.join(os.getcwd(), "results")
# energy = pd.DataFrame()
# for dir in os.listdir(path):
#     if dir != "plots":
#         df = pd.read_csv(
#             os.path.join(path, dir, "output", "DE-electricity.csv"), parse_dates=True,
#             index_col=0
#         )
#         energy = pd.concat([energy, df.clip(0).sum()/1e6], axis=1)


scenarios = pd.read_csv("documentation/scenarios-literature.csv", index_col=[0,1])
scenarios.index = scenarios.index.droplevel(1)
demand = scenarios.loc["demand"]
scenarios = scenarios.drop(["demand", "import", "other-res"])

ax =scenarios.T.plot(kind="bar",  grid=True, color=[color_dict.get(c) for c in scenarios.index])
lgd = ax.legend(loc='lower left', bbox_to_anchor= (0.0, 1.02), ncol=2,
            borderaxespad=0, frameon=False)
ax.set_ylabel("Installed capacity in GW")
plt.xticks(rotation=45)

ax2 = ax.twinx()
ax2 = demand.plot(linestyle="", marker="o", color="salmon")
ax2.set_ylabel("Demand in TWh")
ax2.set_ylim([0, 820])
ax2.set_xlim([-.5, 5.5])

plt.savefig("documentation/scenario-comparison.pdf", bbox_extra_artists=(lgd,), bbox_inches='tight')
