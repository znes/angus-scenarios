import os
import pandas as pd

# import numpy as np

# import plotly.io as pio
import plotly.offline as offline

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
    "chp-must-run"
]

bus = "DE"
base_scenarios = ["2050REF", "2050NB", "2040DG", "2040GCA",  "2030DG", "2030NEPC"]
# GS = [b + "-GS" for b in base_scenarios]
# base_scenarios = base_scenarios + GS

exclude = []

interactive_figures = os.path.join("documentation", "figures", "interactive")
if not os.path.exists(interactive_figures):
    os.makedirs(interactive_figures)

# emissions -------------------------------------------------------------------
emissions = pd.DataFrame()
for dir in os.listdir(path):
    if dir not in exclude:
        df = pd.read_csv(
            os.path.join(path, dir, "emissions.csv"),
            index_col=0,
            parse_dates=True,
        )
        summ = df.sum()
        summ.name = dir
        emissions = pd.concat([emissions, summ], axis=1, sort=False)

total_emissions = emissions.sum() / 1e6
bus_emissions = (emissions.loc[bus + "-electricity"] / 1e6).round(2)
bus_emissions.name = "CO2"
bus_emissions = bus_emissions.sort_index()

# re shares -------------------------------------------------------------------
electricity_demand = {}
shares_supply = {}
shares_demand = {}
excess = {}
for dir in os.listdir(path):
    if dir not in exclude:

        df = pd.read_csv(
            os.path.join(path, dir, "output", bus + "-electricity.csv"),
            index_col=0,
            parse_dates=True,
        )
        sums = df.clip(0).sum().to_dict()
        total_supply = sum(
            sums.get(bus + "-" + k, 0) for k in renewables + conventionals
        )
        re_supply = sum(sums.get(bus + "-" + k, 0) for k in renewables)
        excess[dir] = df[bus + "-electricity-excess"].sum() / 1e6
        shares_demand[dir] = (re_supply - excess[dir]) / df[
            [
                bus + "-flex-decentral_heat-hp",
                bus + "-decentral_heat-hp",
                bus + "-electricity-load",
            ]
        ].sum().sum()
        shares_supply[dir] = (re_supply - excess[dir]) / total_supply

        electricity_demand[dir] = df[
            [
                bus + "-flex-decentral_heat-hp",
                bus + "-decentral_heat-hp",
                bus + "-electricity-load",
            ]
        ].sum()


shares = pd.Series(shares_supply).sort_index()
indicators = pd.concat(
    [
        pd.Series(shares[base_scenarios], name="RES"),
        bus_emissions[base_scenarios],
    ],
    axis=1,
)

indicators = indicators.sort_values(by="CO2", ascending=False)
ax = indicators["CO2"].plot(linestyle="", marker="o", color="skyblue")
ax.set_ylabel("CO2 Emissions in Mio. tons")
ax.set_ylim(0, 210)

plt.xticks(rotation=45)
ax2 = ax.twinx()
indicators["RES"].plot(linestyle="", marker="o", color="darkred", label = 'RES')
ax2.set_ylim(0, 1.1)
ax2.set_ylabel("RE share")

lines, labels = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(
    lines + lines2, labels + labels2, loc="lower left",
    borderaxespad=0,
    frameon=False)

ax.grid(linestyle="--", color="lightgray")
plt.savefig(
    "documentation/figures/scenario-indicators.pdf"
)

# heat system investment ------------------------------------------------------
heat = {}
for dir in os.listdir(path):
    if not "flex" in dir:
        filling = pd.read_csv(
            os.path.join(path, dir, "output", "filling_levels.csv"),
            index_col=0,
            parse_dates=True,
        )["DE-flex-decentral_heat-tes"].max()
        demand = pd.read_csv(
            os.path.join(path, dir, "output", "DE-flex-decentral_heat-bus.csv"),
            index_col=0,
            parse_dates=True,
        )["DE-flex-decentral_heat-load"].max()
        df = pd.read_csv(
            os.path.join(path, dir, "output", "DE-electricity.csv"),
            index_col=0,
            parse_dates=True,
        )
        capacity = pd.read_csv(
            os.path.join(path, dir, "output", "capacities.csv"),
            index_col=[0, 1, 2, 3, 4],
        )
        hp = capacity.loc[
            (
                "DE-flex-decentral_heat-hp",
                "DE-flex-decentral_heat-bus",
                "invest",
                "hp",
                "flex-decentral_heat",
            ),
            "value",
        ]
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
        heat[dir] = (filling / tes, tes/1e3, filling/1e3, hp/1e3, demand/1e3)


investment = pd.DataFrame(heat)
investment.index = ["Ratio", "TES GW", "TES GWh", "HP GW", "Peak Load GW"]
investment[base_scenarios].T.round(2)
investment.sort_index(inplace=True)

inv = investment.drop("Ratio")
ax = inv[base_scenarios].plot(kind="bar", cmap=plt.get_cmap("YlGn"))
ax.set_ylabel("Investment in GW, GWh")
ax.grid(linestyle="--", color="lightgray")
plt.xticks(rotation=45)
plt.savefig(
    "documentation/figures/heat-investment.pdf"
)


fig, ax = plt.subplots()
#base_scenarios = investment.index
ax.scatter(
    y=investment.loc["Ratio"][base_scenarios], x=shares.loc[base_scenarios], color="purple"
)
ax.set_xlim(0.55, 1.05)
ax.set_ylim(2.5, 6)
ax.grid(linestyle="--", color="lightgray")
ax.set_ylabel("Ratio of storage capacity to capacity of the TES")
ax.set_xlabel("RE share")
for i,j in investment[base_scenarios].iteritems():
    ax.annotate(i, (shares[i], investment.at["Ratio", i]))
plt.savefig(
    "documentation/figures/heat-investment-storage-ratio.pdf"
)


# filling levels --------------------------------------------------------------
for dir in os.listdir(path):
    if dir not in exclude:
        filling_levels = pd.read_csv(
            os.path.join(path, dir, "output", "filling_levels.csv"),
            index_col=[0],
            parse_dates=True,
        )
        offline.plot(
            filling_level_plot(
                df,
                scenario=dir,
                bus=bus,
                storages=storages + ["hydro-reservoir"],
                color_dict=color_dict,
            ),
            filename=os.path.join(
                interactive_figures, dir + "-filling-levels.html"
            ),
            auto_open=False,
        )

# hourly plots ---------------------------------------------------------------
for dir in os.listdir(path):
    if dir not in exclude:
        supply_demand = pd.read_csv(
            os.path.join(
                path, dir, "output", "-".join([bus, "electricity"]) + ".csv"
            ),
            index_col=[0],
            parse_dates=True,
        )

        offline.plot(
            hourly_plot(
                supply_demand,
                scenario=dir,
                bus=bus,
                color_dict=color_dict,
                conventionals=conventionals,
                storages=storages,
            ),
            filename=os.path.join(
                interactive_figures, dir + "-hourly-dispatch.html"
            ),
            auto_open=False,
        )

# stacked plot ---------------------------------------------------------------
for dir in os.listdir(path):
    if dir not in exclude:
        capacities = pd.read_csv(
            os.path.join(path, dir, "output", "capacities.csv"), index_col=0
        )
        capacities.set_index("to", append=True, inplace=True)
        capacities = capacities.drop(
            index="DE-decentral_heat-bus", level=1
        ).reset_index(1)
        capacities = (
            capacities.groupby(["to", "carrier", "tech"]).sum().unstack("to")
        )
        capacities.index = ["-".join(i) for i in capacities.index]
        capacities.columns = capacities.columns.droplevel(0)

        offline.plot(
            stacked_plot(capacities, scenario=dir, color_dict=color_dict),
            filename=os.path.join(
                interactive_figures, dir + "-installed-apacities.html"
            ),
            auto_open=False,
        )

# stacked capacities by bus --------------------------------------------------
_df = pd.DataFrame()
for dir in os.listdir(path):
    if dir not in exclude:
        capacities = pd.read_csv(
            os.path.join(path, dir, "output", "capacities.csv"), index_col=0
        )
        capacities.set_index("to", append=True, inplace=True)
        capacities = capacities.xs(bus + "-electricity", level=1)
        capacities.index = [i.replace(bus + "-", "") for i in capacities.index]

        value = capacities["value"]
        value.name = dir
        _df = pd.concat([_df, value], axis=1, sort=False)


offline.plot(
    stacked_plot(_df, scenario=dir, color_dict=color_dict),
    filename=os.path.join(
        interactive_figures, bus + "-installed-apacities.html"
    ),
    auto_open=False,
)

# matplotlib  static figure
_df = _df[[c for c in _df.columns if not "flex" in c]]
conv = [c for c in conventionals if c in _df.index]
_df.loc["fossil"] = _df.loc[conv].sum()
_df = _df.drop(conv)

stor = [c for c in storages if c in _df.index]
_df.loc["storage"] = _df.loc[stor].sum()
_df = _df.drop(stor)

de = _df / 1000
de.sort_index(axis=1, inplace=True)
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

# plt.plot(figsize=(10, 5))
plt.savefig(
    "documentation/figures/" + bus + "-installed_capacities.pdf",
    bbox_extra_artists=(lgd,),
    figsize=(15, 8),
    bbox_inches="tight",
)

# sceanrio data ---------------------------------------------------------------
scenarios = pd.DataFrame()
for dir in os.listdir(path):
    if dir not in exclude:
        df = pd.read_csv(
            os.path.join(path, dir, "output", bus + "-electricity.csv"),
            index_col=0,
            parse_dates=True,
        )

        cols = [
            ("-").join([bus, ct])
            for ct in [
                "electricity-load",
                "electricity-excess",
                "flex-decentral_heat-hp",
                "decentral_heat-hp",
            ]
            if ("-").join([bus, ct]) in df.columns
        ]

        df[cols] = df[cols] * -1

        pos = df.clip(lower=0).sum()
        neg = df.clip(upper=0).sum()
        neg = neg.loc[neg < 0]
        neg.index = [i + "-cos" for i in neg.index]

        df = pd.concat([pos, neg], sort=False)

        # if bus + "-decentral_heat-hp" in df.index:
        #     df.drop(bus + "-decentral_heat-hp", inplace=True)
        df.name = dir

        scenarios = pd.concat([scenarios, df], axis=1, sort=False)

scenarios.fillna(0, inplace=True)
scenarios
scenarios = (scenarios / 1e6).round(2)
scenarios.index = [
    "-".join(i.split("-")[1:]) if not "import" in i else i
    for i in scenarios.index
]

storages_cos = [i + "-cos" for i in scenarios.index if i in storages]

storages = [s for s in storages if s in scenarios.index]
scenarios.loc["storage"] = scenarios.loc[storages].sum()
scenarios.loc["storage-cos"] = scenarios.loc[storages_cos].sum()

scenarios.drop(storages, inplace=True)
scenarios.drop(storages_cos, inplace=True)

scenarios.sort_index(axis=1, inplace=True)

# energy plot ----------------------------------------------------------------
scenarios_plot = scenarios[[c for c in scenarios.columns if not "flex" in c]]
ax = scenarios_plot.T.plot(
    kind="bar",
    stacked=True,
    color=[color_dict.get(i.replace("-cos", "")) for i in scenarios.index],
    label=[i if not "-cos" in i else None for i in scenarios.index],
)
ax.legend()
handles, labels = ax.get_legend_handles_labels()
lgd = {k: v for k, v in dict(zip(handles, labels)).items() if "-cos" not in v}
lgd = ax.legend(
    lgd.keys(),
    lgd.values(),
    loc="lower left",
    bbox_to_anchor=(-0.2, -0.65),
    ncol=4,
    borderaxespad=0,
    frameon=False,
)
ax.set_ylabel("Energy in TWh")
ax.grid(linestyle="--", lw=0.5)
plt.xticks(rotation=45)
# plt.plot(figsize=(10, 5))
plt.savefig(
    "documentation/figures/" + bus + "-aggregated_supply_demand.pdf",
    bbox_extra_artists=(lgd,),
    bbox_inches="tight",
)

offline.plot(
    energy_plot(scenarios_plot, color_dict=color_dict),
    image="svg",
    image_filename=os.path.join(
        interactive_figures, bus + "-aggregated_supply_demand"
    ),
    auto_open=True,
)

#
# fig, axs = plt.subplots(1, 1, sharex=True, sharey=True, figsize=(5,7))
#
# for base_scenario in ["2050NB-", "2050ANGUS-", "2040ST-", "2040GCA-", "2030ST-", "2030DG-"]:
#     scenarios_select = scenarios[[c for c in scenarios.columns if base_scenario in c]]
#     x=list(scenarios_select.columns)
#     x.sort()
#     x.sort(key=len)
#     ref = (scenarios_select)
#     ref.rename(index={"import-cos": "export"}, inplace=True)
#     ax = ref.loc["storage", x].T.plot(linestyle="-.", label=base_scenario)
# ax.grid(linestyle="--", color="lightgray")
# ax.set_ylabel("Relative difference")
# ax.set_xlabel("Share of flexibilisation")
# ax.spines['top'].set_visible(False)
# ax.spines['right'].set_visible(False)
# ax.set_xlim(0, 10)
# plt.xticks(rotation=45)
# lgd = ax.legend(
#     title="",
#     loc="upper right",
#     bbox_to_anchor=(1, 1.1),
#     ncol=3,
#     borderaxespad=0,
#     frameon=False,
# )
# plt.savefig(
#     "documentation/figures/relative-deviation-0-100.pdf",
#     bbox_inches="tight",
# )
# sns.despine(left=True, bottom=True)

# scenario comparision flex / no flex -----------------------------------------
base = [
    c for c in scenarios.columns if "flex0" in c
]  # and not "flex100" in c]
comparison = {}
if False:  # for relative
    for c in base:
        comparison[c] = (
            scenarios[c] / scenarios[c.replace("-flex0", "")] - 1
        ).to_dict()
    comparison = pd.DataFrame(comparison)
    comparison.rename(
        index={"import-cos": "export", "electricity-excess-cos": "excess"},
        inplace=True,
    )
    name = "Relative Deviation"
else:
    for c in base:
        comparison[c.replace("-flex0", "")] = (
            scenarios[c] - scenarios[c.replace("-flex0", "")]
        ).to_dict()
    comparison = pd.DataFrame(comparison)
    comparison.rename(
        index={"import-cos": "export", "electricity-excess-cos": "excess"},
        inplace=True,
    )
    comparison.loc[["export", "excess"]] = (
        comparison.loc[["export", "excess"]] * -1
    )
    name = "Absoltue Deviation in TWh"
comparison = (
    comparison.loc[["import", "export", "storage", "excess"]].round(3).T
)
comparison = comparison.stack()
comparison = comparison.to_frame()
comparison.reset_index(inplace=True)

# sns.set_palette("RdBu_r", 6)
ax = sns.barplot(
    x="level_0", y=0, hue="level_1", data=comparison, palette="YlGnBu"
)

sns.despine(left=True, bottom=True)
ax.grid(linestyle="--", color="gray")
ax.set_ylabel(name)
ax.set_xlabel("Scenario")

plt.xticks(rotation=45)
lgd = ax.legend(
    title="",
    loc="upper right",
    bbox_to_anchor=(1, 1.1),
    ncol=4,
    borderaxespad=0,
    frameon=False,
)
shares_ = shares[[c for c in scenarios.columns if not "flex" in c]]

ax2 = ax.twinx()
ax2.set_ylim(0, 1)
plt.plot(shares_.index, shares_, "o")
ax2.set_ylabel("RE share")

plt.savefig(
    "documentation/figures/absolute-deviation.pdf",
    bbox_extra_artists=(lgd,),
    bbox_inches="tight",
)


# literature scenarios comparison ---------------------------------------------
scenarios = pd.read_csv(
    "documentation/data/scenarios-literature.csv", index_col=[0, 1]
)
scenarios.index = scenarios.index.droplevel(1)
demand = scenarios.loc["demand"]
scenarios = scenarios.drop(["demand", "import", "other-res"])

ax = scenarios.T.plot(
    kind="bar", grid=True, color=[color_dict.get(c) for c in scenarios.index]
)
lgd = ax.legend(
    loc="lower left",
    bbox_to_anchor=(0.0, 1.02),
    ncol=2,
    borderaxespad=0,
    frameon=False,
)
ax.set_ylabel("Installed capacity in GW")
plt.xticks(rotation=45)

ax2 = ax.twinx()
ax2 = demand.plot(
    linestyle="", marker="o", color=color_dict.get("electricity-load")
)
ax2.set_ylabel("Demand in TWh")
ax2.set_ylim([0, 820])
ax2.set_xlim([-0.5, 5.5])

plt.savefig(
    "documentation/figures/scenario-comparison.pdf",
    bbox_extra_artists=(lgd,),
    bbox_inches="tight",
)


# shadow prices ---------------------------------------------------------------
sorted = {}
unsorted = {}
for dir in os.listdir(path):
    if dir not in exclude:
        data_path = os.path.join(path, dir, "output", "shadow_prices.csv")
        sprices = pd.read_csv(data_path, index_col=[0], parse_dates=True)[
            bus + "-electricity"
        ]
        sorted[dir] = sprices.sort_values().values
        unsorted[dir] = sprices.values

renewables = ["wind-onshore", "wind-offshore", "solar-pv", "hydro-ror"]
timestamps = {}
shadow_prices = {}
rload = {}
for dir in os.listdir(path):
    if dir not in exclude:
        data_path = os.path.join(path, dir, "output", bus + "-electricity.csv")
        country_electricity_df = pd.read_csv(
            data_path, index_col=[0], parse_dates=True
        )
        country_electricity_df["rload"] = country_electricity_df[
            ("-").join([bus, "electricity-load"])
        ] - country_electricity_df[
            [("-").join([bus, i]) for i in renewables]
        ].sum(
            axis=1
        )

        rload[dir] = country_electricity_df["rload"].values
        timestamps[dir] = country_electricity_df.index

tuples = {
    (0, 0): ("2030NEPC-flex0", "2030NEPC"),
    (0, 1): ("2040DG-flex0", "2040DG"),
    (0, 2): ("2050REF-GS-flex0", "2050REF-GS"),
}
fig, axs = plt.subplots(1, 3, sharex=True, sharey=True, figsize=(15, 5))

for k, values in tuples.items():
    for v in values:
        axs[k[1]].scatter(
            rload[v] / 1e3, unsorted[v], s=1, marker="o", label=v
        )
        # axs.hist(unsorted[v], label=v)
        axs[k[1]].set_ylim(-10, 150)
        axs[k[1]].grid(True, linestyle="--", color="lightgray")

        axs[k[1]].set_ylabel("Shadwo price in \n Euro / MWh")

        # ax = sns.jointplot(x="x", y="y", data=df, kind="kde")
        # axs[k[1]].spines['top'].set_visible(False)
        # axs[k[1]].spines['right'].set_visible(False)
        lgd = axs[k[1]].legend(
            title="",
            loc="upper left",
            # bbox_to_anchor=(1, 1),
            ncol=2,
            borderaxespad=0,
            frameon=False,
        )

axs[k[1]].set_xlabel("Residual load in GW")
axs[k[0]].set_xlabel("Residual load in GW")

plt.suptitle("Shadow prices vs. Residual load")
# plt.ylim(-10, 200)
plt.savefig(
    "documentation/figures/shadow-prices-vs-rload.pdf", bbox_inches="tight"
)

# boxplot for prices  --------------------------------------------------------
x = pd.DataFrame(unsorted, index=timestamps["2050REF"])[
    ["2050REF-flex0", "2050REF"]
]
x = pd.concat([x.loc[x.index.month == i] for i in range(1, 13)], axis=1)

df = pd.DataFrame(unsorted)[base_scenarios]
df.columns = [i.replace("flex", "") for i in df.columns]
df = df.sort_index(axis=1)
ax = df.boxplot(flierprops=dict(markerfacecolor="r", marker="+"))
ax.set_ylim(-10, 220)
ax.grid(True, linestyle="--", color="lightgray")
ax.set_ylabel("Shadow price in Euro / MWh")
plt.xticks(rotation=45)

# plt.suptitle("Shadow prices within different scenarios")

plt.savefig(
    "documentation/figures/boxplot-shadow-prices.pdf", bbox_inches="tight"
)

# comparison of transmission -------------------------------------------------
exchange_df = pd.DataFrame()
bus = "DE"
compare = ("2050REF-flex0", "2050REF")
for dir in os.listdir("results"):
    if dir in compare:
        tr = pd.read_csv(
            os.path.join(path, dir, "output", "transmission.csv"),
            sep=",",
            index_col=0,
            parse_dates=True,
            header=[0, 1, 2],
        )

        imports = tr.loc[:, (slice(None), bus + "-electricity")]
        imports.columns = imports.columns.droplevel(["type", "to"])
        imports.columns = [
            c.replace(bus + "-electricity", "") for c in imports
        ]
        exports = tr.loc[:, (bus + "-electricity")]
        exports.columns = exports.columns.droplevel("type")
        exports.columns = [
            c.replace(bus + "-electricity", "") for c in exports
        ]
        exchange = imports - exports
        exchange["scenario"] = dir
        exchange.set_index("scenario", append=True, inplace=True)
        exchange_df = pd.concat([exchange_df, exchange])


im = exchange_df.sum(axis=1).clip(lower=0)
im = im.unstack()
im = im[compare[1]] - im[compare[0]]
im = im[~((im - im.mean()).abs() > 3 * im.std())]
im = im.to_frame()
im["day"] = im.index.dayofyear.values
im["hour"] = im.index.hour.values
im.set_index(["hour", "day"], inplace=True)
im = im.unstack("day")
im = im.droplevel(0, axis=1)
im.sort_index(ascending=True, inplace=True)

ex = exchange_df.sum(axis=1).clip(upper=0)
ex = ex.unstack() * -1
ex = ex[compare[1]] - ex[compare[0]]
ex = ex[~((ex - ex.mean()).abs() > 3 * ex.std())]
ex = ex.to_frame()
ex["day"] = ex.index.dayofyear.values
ex["hour"] = ex.index.hour.values
ex.set_index(["hour", "day"], inplace=True)
ex = ex.unstack("day")
ex = ex.droplevel(0, axis=1)
ex.sort_index(ascending=True, inplace=True)

fig, axs = plt.subplots(2, 1)
im = im / 1e3
ex = ex / 1e3

vmax = max(ex.max().max(), im.max().max())
vmin = min(ex.min().min(), im.min().min())
axs[0] = sns.heatmap(
    data=im,
    xticklabels=False,
    yticklabels=4,
    cmap="RdYlBu",
    # vmax=vmax,
    # vmin=vmin,
    ax=axs[0],
    cbar_kws={"label": "Import in GW"},
)
axs[1] = sns.heatmap(
    data=ex,
    xticklabels=40,
    yticklabels=4,
    cmap="RdYlBu",
    # vmax=vmax,
    # vmin=vmin,
    ax=axs[1],
    cbar_kws={"label": "Export in GW"},
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
    "documentation/figures/heat-plot-{}.pdf".format(compare[0]),
    # bbox_extra_artists=(lgd,),
    bbox_inches="tight",
)

# sorted transmission duration ------------------------------------------------
sorted_exchange = pd.DataFrame(
    {c: sorted(exchange_df[c].values) for c in exchange_df.columns}
)
sorted_exchange.columns = [
    c.strip("-electricity") for c in sorted_exchange.columns
]
data = sorted_exchange.stack().to_frame()
data.index.names = ["t", "ctr"]
data.reset_index(inplace=True)
sns.set_palette("cubehelix", 11)
ax = sns.lineplot(x="t", y=0, hue="ctr", data=data)
ax.grid(linestyle="--", color="gray")
ax.set_ylabel("Tranmission in GW")
ax.set_xlabel("Hours")
lgd = ax.legend(
    title="",
    # loc="upper left",
    bbox_to_anchor=(1.1, 1.3),
    ncol=4,
    borderaxespad=0,
    frameon=False,
)
plt.savefig(
    "documentation/figures/transmission.pdf",
    bbox_extra_artists=(lgd,),
    bbox_inches="tight",
)
