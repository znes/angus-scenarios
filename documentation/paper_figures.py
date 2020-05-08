import os
import pandas as pd
from cydets.algorithm import detect_cycles

## import numpy as np

# import plotly.io as pio
import plotly.offline as offline
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import seaborn as sns
from documentation.plotly_plots import (
    filling_level_plot,
    hourly_plot,
    stacked_plot,
    energy_plot,
)


color = {
    "conventional": "dimgrey",
    "cavern-acaes": "crimson",
    "redox-battery": "violet",
    "lignite-st": "sienna",
    "coal-st": "dimgrey",
    "uranium-st": "yellow",
    "gas-ocgt": "gray",
    "gas-ccgt": "lightgray",
    "solar-pv": "lightyellow",
    "wind-onshore": "skyblue",
    "wind-offshore": "steelblue",
    "biomass-st": "yellowgreen",
    "hydro-ror": "aqua",
    "hydro-phs": "purple",
    "hydro-reservoir": "magenta",
    "hydro-rsv": "magenta",
    "hydrogen-storage": "pink",
    "lithium-battery": "salmon",
    "waste-st": "yellowgreen",
    "oil-ocgt": "black",
    "other": "red",
    "other-res": "orange",
    "electricity-load": "slategray",
    "import": "mediumpurple",
    "storage": "plum",
    "mixed-st": "chocolate",
    "decentral_heat-hp": "darkcyan",
    "flex-decentral_heat-hp": "darkcyan",
    "fossil": "darkgray",
}
color_dict = {name: colors.to_hex(color) for name, color in color.items()}

path = os.path.join(os.getcwd(), "results")

renewables = [
    "hydro-ror",
    "hydro-reservoir",
    "wind-offshore",
    "wind-onshore",
    "solar-pv",
    "other-res",
    "biomass-st",
]
storages = [
    "hydrogen-storage",
    "redox-battery",
    "hydro-phs",
    "cavern-acaes",
    "lithium-battery",
]
conventionals = [
    "lignite-st",
    "gas-ccgt",
    "mixed-st",
    "gas-ocgt",
    "coal-st",
    "oil-ocgt",
    "uranium-st",
    "waste-st",
    "chp-must-run",
]

bus = "DE"
base_scenarios = ["2050REF", "2040DG", "2040GCA", "2030DG"]


heat = {}
peak_demand = {}
heat_storage = {}
heat_bus = {}
for dir in os.listdir(path):
    if not "flex" in dir:
        filling = pd.read_csv(
            os.path.join(path, dir, "output", "filling_levels.csv"),
            index_col=0,
            parse_dates=True,
        )["DE-flex-decentral_heat-tes"].max()
        heat_bus[dir] = pd.read_csv(
            os.path.join(
                path, dir, "output", "DE-flex-decentral_heat-bus.csv"
            ),
            index_col=0,
            parse_dates=True,
        )

        peak_demand[dir] = heat_bus[dir]["DE-flex-decentral_heat-load"].max()

        heat_storage[dir] = (
            heat_bus[dir]["DE-flex-decentral_heat-tes"].clip(0).sum() / 1e6
        )

        df = pd.read_csv(
            os.path.join(path, dir, "output", "DE-electricity.csv"),
            index_col=0,
            parse_dates=True,
        )
        capacity = pd.read_csv(
            os.path.join(path, dir, "output", "capacities.csv"),
            index_col=[0, 1, 2, 3, 4],
        )

        hp = (
            capacity.loc[
                (
                    "DE-flex-decentral_heat-gshp",
                    "DE-flex-decentral_heat-bus",
                    "invest",
                    "gshp",
                    "flex-decentral_heat",
                ),
                "value",
            ]
            + capacity.loc[
                (
                    "DE-flex-decentral_heat-gshp",
                    "DE-flex-decentral_heat-bus",
                    "capacity",
                    "gshp",
                    "flex-decentral_heat",
                ),
                "value",
            ]
        )

        tes = capacity.loc[
            (
                "DE-flex-decentral_heat-tes",
                "DE-flex-decentral_heat-bus",
                "invest",
                "tes",
                "decentral_heat",
            ),
            "value",
        ]

        heat[dir] = (tes, filling, hp)


investment = pd.DataFrame(heat) / 1e3
investment.index = ["TES (GW)", "TES (GWh)", "HP (GW)"]
investment[base_scenarios].T.round(2)
investment.sort_index(inplace=True)

investment.loc["TES (GWh)"] / investment.loc["HP (GW)"]
# inv.loc["TES (GWh)"] / inv.loc["P. Load (GW)"]
inv = investment[base_scenarios]
x = list(inv.columns)
x.sort()
ax = inv[x].plot(kind="bar", cmap=plt.get_cmap("coolwarm"))
ax.set_ylabel("Investment in GW(h)")
lgd = ax.legend(
    loc="upper left",
    # bbox_to_anchor=(-0.05, -0.45),
    # shadow=False,
    # frameon=False,
    ncol=2,
)
ax.set_ylim(0, 170)
plt.xticks(rotation=0)
ax.grid(linestyle="--", lw=0.5, color="lightgray")


plt.savefig(
    "documentation/figures/heat-investment.pdf",
    bbox_extra_artists=(lgd,),
    bbox_inches="tight",
)

# electricity storage investment ---------------------------------------------
elstorage = {}
for dir in os.listdir(path):
    capacity = pd.read_csv(
        os.path.join(path, dir, "output", "capacities.csv"),
        index_col=[0, 1, 2, 3, 4],
    )

    for bus in [
        "AT",
        "BE",
        "CH",
        "CZ",
        "DE",
        "DK",
        "FR",
        "NL",
        "LU",
        "NO",
        "PL",
        "SE",
    ]:
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
        elstorage[(bus, dir)] = (lithstor, hydstor)

elstorage = pd.DataFrame(elstorage)
elstorage = elstorage.xs("DE", level=0, axis=1)

# biomass potenteial sensitivity ---------------------------------------------
scenario = "2050REF-bio"
bio_cols = [c for c in elstorage.columns if scenario in c]
bio = elstorage[bio_cols]
bio_investment = investment[[c for c in bio_cols if not "flex" in c]]
bio_investment.columns = [
    c.replace(scenario + "-", "") for c in bio_investment.columns
]
bio.index = ["Lithium", "Hydrogen"]
bio = bio / 1e3
bioflex0 = bio[[c for c in bio.columns if "flex0" in c]]
bioflex0.columns = [c.replace("-flex0", "") for c in bioflex0.columns]
bioflex100 = bio[[c for c in bio.columns if not "flex0" in c]]
bioflex0.columns = [c.replace(scenario + "-", "") for c in bioflex0.columns]
bioflex100.columns = [
    c.replace(scenario + "-", "") for c in bioflex100.columns
]

# (elstorage.loc[0, "2050REF-bio-0"]  - elstorage.loc[0, "2050REF"]) / elstorage.loc[0, "2050REF"] * 100
x = list(bioflex0.columns)
x.sort()
x.sort(key=len)
x = [str(x) for x in [0, 20, 40, 60, 80]]
ax = bioflex0[x].T.plot(marker="*", color=["m", "skyblue"])
bioflex100.index = [i + "-flex" for i in bioflex100.index]
bioflex100[x].T.plot(ax=ax, linestyle="--", marker="*", color=["m", "skyblue"])
ax.set_xticks(range(5))
ax.set_xticklabels(["{}".format(int(150.2 * int(i) / 100)) for i in x])
ax.grid(linestyle="--", lw=0.5, color="lightgray")
# ax.set_ylim(0, 38)
ax.axvline(x=1.5, ymin=0.0, ymax=40, color="black", lw=1)
ax.set_ylabel("Investment in GW")
ax.set_xlabel("Biomass potential in TWh")
ax.legend(loc=0, labels=["Li", "Hy", "Li-flex", "Hy-flex"], ncol=2)

ax2 = ax.twinx()
ax2.set_ylabel("Change in TES (GWh) investment in %")
(
    -100
    * (
        bio_investment.loc["TES (GWh)", "0"]
        - bio_investment.loc["TES (GWh)", x]
    )
    / bio_investment.loc["TES (GWh)", "0"]
).plot(ax=ax2, color="orange", marker="o", linestyle="")
# bio_investment.loc["TES (GWh)", x].plot(ax=ax2, color="orange", marker="o", linestyle="")
ax2.set_ylim(-25, 25)
ax2.legend(loc=3, labels=["TES"])
ax.set_xticklabels(["{}".format(int(150.2 * int(i) / 100)) for i in x])
plt.savefig(
    "documentation/figures/bio-{}-sensitivity.pdf".format(scenario),
    bbox_inches="tight",
)

# load sensitivity plot -------------------------------------------------------
scenario = "2050REF-load"
load_cols = [c for c in elstorage.columns if scenario in c]
load = elstorage[load_cols]
load_investment = investment[[c for c in load_cols if not "flex" in c]]
load_investment.columns = [
    c.replace("2050REF-load-", "") for c in load_investment.columns
]
load.index = ["Lithium", "Hydrogen"]
load = load / 1e3
loadflex0 = load[[c for c in load.columns if "flex0" in c]]
loadflex0.columns = [c.replace("-flex0", "") for c in loadflex0.columns]
loadflex100 = load[[c for c in load.columns if not "flex0" in c]]
loadflex0.columns = [c.replace(scenario + "-", "") for c in loadflex0.columns]
loadflex100.columns = [
    c.replace(scenario + "-", "") for c in loadflex100.columns
]
elstorage["2050REF-flex0"]

x = list(loadflex0.columns)
x.sort()
x.sort(key=len)
x = [int(i) for i in reversed(x)]
x.sort()
x = [str(i) for i in x]


# ax = (loadflex0[x].T.sub(loadflex0["0"]).divide(loadflex0["0"])).plot(marker="*", color=["m", "skyblue"])
ax = loadflex0[x].T.plot(marker="*", color=["m", "skyblue"])
loadflex100.index = [i + "-flex" for i in loadflex100.index]
loadflex100[x].T.plot(
    ax=ax, linestyle="--", marker="*", color=["m", "skyblue"]
)
# ax = (loadflex100[x].T.sub(loadflex100["0"]).divide(loadflex100["0"])).plot(ax=ax, linestyle="--", marker="*", color=["m", "skyblue"])

ax.set_xticks(range(7))
ax.set_xticklabels([str(i) for i in x])
ax.grid(linestyle="--", lw=0.5, color="lightgray")
# ax.set_ylim(0, 10)
ax.axvline(x=3, ymin=0.0, ymax=40, color="black", lw=1)
ax.set_ylabel("Investment in GW")
ax.set_xlabel("Change in heat load in % ")
ax.legend(loc=0, labels=["Li", "Hy", "Li-flex", "Hy-flex"], ncol=2)

ax2 = ax.twinx()
ax2.set_ylabel("Change in TES (GWh) investment in %")
(
    -100
    * (
        load_investment.loc["TES (GWh)", "0"]
        - load_investment.loc["TES (GWh)", x]
    )
    / load_investment.loc["TES (GWh)", "0"]
).plot(ax=ax2, color="orange", marker="o", linestyle="")

# x = ( -100 *
#     (load_investment.loc["TES (GWh)", "0"] - load_investment.loc["TES (GWh)", x]) /
#     load_investment.loc["TES (GWh)", "0"])
# x.reset_index()
ax2.set_ylim(-25, 25)
ax2.legend(loc=4, labels=["TES"])

# load_investment.loc["TES (GWh)", x].plot(ax=ax2, color="orange", marker="o", linestyle="")

plt.savefig(
    "documentation/figures/load-{}-sensitivity.pdf".format(scenario),
    bbox_inches="tight",
)

a = elstorage.xs("2050REF", level=1, axis=1)
b = elstorage.xs("2050REF-flex0", level=1, axis=1)
ax = (
    a.sub(b)
    .T.divide(1e3)
    .plot(kind="barh", stacked=False, color=["m", "skyblue"])
)


# storage investment plot -----------------------------------------------------
elstorage.index = ["Lithium", "Hydrogen"]
flex0 = elstorage[[c for c in elstorage.columns if "flex" in c]]
flex100 = elstorage[[c for c in elstorage.columns if not "flex" in c]]
flex0.columns = [c.replace("-flex0", "") for c in flex0.columns]
add = flex0.sub(flex100)  #
add.index = [i + "-inv" for i in add.index]
df = pd.concat([add, flex100], sort=False)
df.sort_index(inplace=True)
df = df / 1e3


base_scenarios.sort()
fig, axs = plt.subplots(1, 2, sharex=True, sharey=True, figsize=(10, 5))

df.loc[[f for f in df.index if "Lithium" in f]][
    [b for b in base_scenarios if b in df.columns]
].T.plot(kind="bar", stacked=True, color=["plum", "m"], ax=axs[0])
axs[0].grid(linestyle="--", lw=0.5, color="lightgray")
df.loc[[f for f in df.index if "Hydro" in f]][
    [b for b in base_scenarios if b in df.columns]
].T.plot(kind="bar", color=["skyblue", "darkblue"], stacked=True, ax=axs[1])
for tick in axs[0].get_xticklabels():
    tick.set_rotation(0)

axs[1].grid(linestyle="--", lw=0.5, color="lightgray")
axs[0].set_ylabel("Investment in GW")
lgd = axs[0].legend()

x = df.loc[[f for f in df.index if "Hydro" in f]][
    [b for b in base_scenarios if b in df.columns]
]
x.iloc[1] / x.sum()
plt.xticks(rotation=0)

plt.savefig(
    "documentation/figures/elec-investment.pdf",
    bbox_extra_artists=(lgd,),
    bbox_inches="tight",
)


# filling levels --------------------------------------------------------------
cycles = {}
cycles_h = {}
cycles_l = {}

for dir in os.listdir(path):
    if dir in base_scenarios:
        df = pd.read_csv(
            os.path.join(path, dir, "output", "filling_levels.csv"),
            index_col=[0],
            parse_dates=True,
        )
        if not "flex" in dir:
            try:
                cycles[dir] = detect_cycles(df["DE-flex-decentral_heat-tes"])
            except:
                pass

for dir in os.listdir(path):
    df = pd.read_csv(
        os.path.join(path, dir, "output", "filling_levels.csv"),
        index_col=[0],
        parse_dates=True,
    )
    if sum(df["DE-hydrogen-storage"] != 0):
        cycles_h[dir] = detect_cycles(df["DE-hydrogen-storage"])
    if sum(df["DE-lithium-battery"] != 0):
        cycles_l[dir] = detect_cycles(df["DE-lithium-battery"])

for v in base_scenarios:
    if v in cycles:
        ax = sns.jointplot(
            x=cycles[v]["duration"] / np.timedelta64(1, "h"),
            y=cycles[v]["doc"],
            marginal_kws=dict(bins=100, rug=True),
            kind="scatter",
            color="darkblue",
            edgecolor="skyblue",
        )
        ax.set_axis_labels(
            "Duration of cycle in h", "Normalised depth of cycle"
        )
        plt.savefig("documentation/figures/cycles-tes-{}.pdf".format(v))
    if v in cycles_l:
        ax = sns.jointplot(
            x=cycles_l[v]["duration"] / np.timedelta64(1, "h"),
            y=cycles_l[v]["doc"],
            marginal_kws=dict(bins=100, rug=True),
            kind="scatter",
            color="m",
            edgecolor="purple",
        )
        ax.set_axis_labels(
            "Duration of cycle in h", "Normalised depth of cycle"
        )
        plt.savefig("documentation/figures/cycles-lithium-{}.pdf".format(v))
    if v in cycles_h:
        ax = sns.jointplot(
            x=cycles_h[v]["duration"] / np.timedelta64(1, "h"),
            y=cycles_h[v]["doc"],
            marginal_kws=dict(bins=100, rug=True),
            kind="scatter",
            color="skyblue",
            edgecolor="darkblue",
        )
        ax.set_axis_labels(
            "Duration of cycle in h", "Normalised depth of cycle"
        )
        plt.savefig("documentation/figures/cycles-hydrogen-{}.pdf".format(v))

# filling levels plain -----
# hydrogen = {}
# select = base_scenarios #+ [b + "-flex0" for b in base_scenarios]
# for dir in os.listdir(path):
#     if dir in select:
#         df = pd.read_csv(
#             os.path.join(path, dir, "output", "filling_levels.csv"),
#             index_col=[0],
#             parse_dates=True,
#         )
#         hydrogen[dir] = df["DE-flex-decentral_heat-tes"].values


# comparison of storage operation -------------------------------------------------

storage_df = pd.DataFrame()
storage_type = "DE-lithium-battery"  # flex-decentral_heat-tes"
bus = "DE-electricity.csv"  # flex-decentral_heat-bus.csv"
compare = ("2050REF-flex0", "2050REF")
for dir in os.listdir("results"):
    if dir in compare:
        storage = pd.read_csv(
            os.path.join(path, dir, "output", bus),
            sep=",",
            index_col=0,
            parse_dates=True,
            header=[0],
        )[storage_type]
        storage = storage.to_frame()
        storage["scenario"] = dir
        storage.set_index("scenario", append=True, inplace=True)
        storage_df = pd.concat([storage, storage_df])

im = storage_df.clip(lower=0)
im = im.unstack()
im.columns = im.columns.droplevel(0)
im = im[compare[1]] - im[compare[0]]


# im = im[~((im - im.mean()).abs() > 3 * im.std())]
im = im.to_frame()
im["day"] = im.index.dayofyear.values
im["hour"] = im.index.hour.values
im.set_index(["hour", "day"], inplace=True)
im = im.unstack("day")
im.columns = im.columns.droplevel(0)

im.sort_index(ascending=True, inplace=True)

ex = storage_df.clip(upper=0)
ex = ex.unstack() * -1
ex.columns = ex.columns.droplevel(0)
ex = ex[compare[1]] - ex[compare[0]]

# ex = ex[~((ex - ex.mean()).abs() > 3 * ex.std())]
ex = ex.to_frame()
ex["day"] = ex.index.dayofyear.values
ex["hour"] = ex.index.hour.values
ex.set_index(["hour", "day"], inplace=True)
ex = ex.unstack("day")
ex.columns = ex.columns.droplevel(0)
ex.sort_index(ascending=True, inplace=True)

fig, axs = plt.subplots(2, 1)
im = im / 1e3
ex = ex / 1e3

vmax = max(ex.max().max(), im.max().max())
vmin = min(ex.min().min(), im.min().min())
# vmax = 8
# vmin = -8
axs[0] = sns.heatmap(
    data=im,
    xticklabels=False,
    yticklabels=4,
    cmap="RdPu",
    vmax=vmax,
    vmin=vmin,
    ax=axs[0],
    cbar_kws={"label": "Discharge in GW"},
)
axs[1] = sns.heatmap(
    data=ex,
    xticklabels=40,
    yticklabels=4,
    cmap="RdPu",
    vmax=vmax,
    vmin=vmin,
    ax=axs[1],
    cbar_kws={"label": "Charge in GW"},
)

for a in axs:
    a.set_yticklabels(axs[1].get_yticklabels(), rotation=0, fontsize=8)
    a.set_xticklabels(axs[1].get_xticklabels(), rotation=0, fontsize=8)
    a.set_ylim(0, 24)
    a.set_xlim(0, 365)
    a.set_ylabel("Hour of Day", fontsize=8)

axs[1].set_xlabel("Day of Year")
axs[0].set_xlabel("")
axs[0].set_xticklabels("")


# plt.suptitle("Transmission Deviation for \n {0} vs. {1}".format(compare[0], compare[1]))
plt.savefig(
    "documentation/figures/"
    + storage_type
    + "-heat-plot-{}.pdf".format(compare[0]),
    # bbox_extra_artists=(lgd,),
    bbox_inches="tight",
)

# re shares -------------------------------------------------------------------
electricity_demand = {}
shares_supply = {}
shares_demand = {}
excess = {}
imports = {}
conv_supply = {}
bus = "DE"
for dir in os.listdir(path):
    if dir in base_scenarios:
        df = pd.read_csv(
            os.path.join(path, dir, "output", bus + "-electricity.csv"),
            index_col=0,
            parse_dates=True,
        )
        sums = df.clip(0).sum().to_dict()
        total_supply = sum(
            sums.get(bus + "-" + k, 0) for k in renewables + conventionals
        )
        conv_supply[dir] = (
            sum(sums.get(bus + "-" + k, 0) for k in conventionals) / 1e6
        )
        imports[dir] = df["import"].clip(0).sum() / 1e6
        re_supply = sum(sums.get(bus + "-" + k, 0) for k in renewables)
        excess[dir] = df[bus + "-electricity-excess"].sum() / 1e6
        shares_demand[dir] = (re_supply - excess[dir]) / df[
            [
                bus + "-flex-decentral_heat-gshp",
                bus + "-decentral_heat-gshp",
                bus + "-electricity-load",
            ]
        ].sum().sum()
        shares_supply[dir] = (re_supply - excess[dir]) / total_supply

        electricity_demand[dir] = df[
            [
                bus + "-flex-decentral_heat-gshp",
                bus + "-decentral_heat-gshp",
                bus + "-electricity-load",
            ]
        ].sum()
shares = pd.Series(shares_supply).sort_index()

# stacked capacities ----------------------------------------------------------

_df = pd.DataFrame()
for dir in os.listdir(path):
    if dir in base_scenarios:
        capacities = pd.read_csv(
            os.path.join(path, dir, "output", "capacities.csv"), index_col=0
        )
        capacities.set_index("to", append=True, inplace=True)
        capacities = capacities.xs(bus + "-electricity", level=1)
        capacities.index = [i.replace(bus + "-", "") for i in capacities.index]

        value = capacities["value"]
        value = value.groupby(
            value.index
        ).sum()  # sum investemnt and existing capacity
        value.name = dir
        _df = pd.concat([_df, value], axis=1, sort=False)

# matplotlib  static figure
_df = _df[base_scenarios]
aux = dict()
for x in shares[base_scenarios].sort_values().index:
    aux[x] = _df[x].values
_df = pd.DataFrame(aux, index=_df.index)

conv = [c for c in conventionals if c in _df.index]
_df.loc["fossil"] = _df.loc[conv].sum()
_df = _df.drop(conv)

stor = [c for c in storages if c in _df.index]
_df.loc["storage"] = _df.loc[stor].sum()
_df = _df.drop(stor)
_df = _df.drop("storage")
_df = _df.drop("other-res")

de = _df / 1000
# de.sort_index(axis=1, inplace=True)
ax = (de.T).plot(
    kind="bar", stacked=True, color=[color_dict.get(c) for c in de.index]
)
lgd = ax.legend(
    loc="lower left",
    bbox_to_anchor=(0, -0.5),
    shadow=False,
    frameon=False,
    ncol=3,
)
ax.set_ylabel("Installed capacity in GW")
ax.grid(linestyle="--", lw=0.2)
plt.xticks(rotation=45)

ax2 = ax.twinx()
ax2.set_ylim(0, 1)
plt.plot(
    shares[base_scenarios].sort_values().index,
    shares[base_scenarios].sort_values(),
    "*",
    color="darkred",
)
ax2.set_ylabel("RE share")

# plt.plot(figsize=(10, 5))
plt.savefig(
    "documentation/figures/" + bus + "-installed_capacities.pdf",
    bbox_extra_artists=(lgd,),
    figsize=(15, 8),
    bbox_inches="tight",
)
