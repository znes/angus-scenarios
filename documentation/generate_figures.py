import os
import pandas as pd
from cydets.algorithm import detect_cycles

## import numpy as np

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
    "decentral_heat-gshp": "darkcyan",
    "flex-decentral_heat-gshp": "darkcyan",
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
base_scenarios = ["2030NEPC", "2050REF", "2040DG", "2040GCA", "2030DG"]

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
imports = {}
conv_supply = {}
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
indicators["RES"].plot(linestyle="", marker="o", color="darkred", label="RES")
ax2.set_ylim(0, 1.1)
ax2.set_ylabel("RE share")

lines, labels = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(
    lines + lines2,
    labels + labels2,
    loc="lower left",
    borderaxespad=0,
    frameon=False,
)

ax.grid(linestyle="--", color="lightgray")
plt.savefig("documentation/figures/scenario-indicators.pdf")


# filling levels --------------------------------------------------------------

for dir in os.listdir(path):
    if dir in base_scenarios:
        if not "flex" in dir:
            df = pd.read_csv(
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
    if dir in base_scenarios:
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
    if dir in base_scenarios:
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


offline.plot(
    stacked_plot(_df, scenario=dir, color_dict=color_dict),
    filename=os.path.join(
        interactive_figures, bus + "-installed-apacities.html"
    ),
    auto_open=False,
)

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
    "o",
)
ax2.set_ylabel("RE share")


# plt.plot(figsize=(10, 5))
plt.savefig(
    "documentation/figures/" + bus + "-installed_capacities.pdf",
    bbox_extra_artists=(lgd,),
    figsize=(15, 8),
    bbox_inches="tight",
)

# scenario data ---------------------------------------------------------------
scenarios = pd.DataFrame()
for dir in os.listdir(path):
    if dir in base_scenarios:
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
                "flex-decentral_heat-gshp",
                "decentral_heat-gshp",
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
scenarios_plot = scenarios[base_scenarios]
scenarios_plot = scenarios_plot[scenarios_plot.columns.sort_values()]
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
    data_path = os.path.join(path, dir, "output", bus + "-electricity.csv")
    country_electricity_df = pd.read_csv(
        data_path, index_col=[0], parse_dates=True
    )
    country_electricity_df["rload"] = country_electricity_df[
        ("-").join([bus, "electricity-load"])
    ] - country_electricity_df[[("-").join([bus, i]) for i in renewables]].sum(
        axis=1
    )

    rload[dir] = country_electricity_df["rload"].values
    timestamps[dir] = country_electricity_df.index

# resiudal load plot ---------------------------------------
rload_df = pd.DataFrame(rload)[base_scenarios] / 1e3
rload_df.sort_index(axis=1, inplace=True)
for c in rload_df[base_scenarios].columns:
    rload_df[c] = rload_df[c].sort_values(ascending=False).values

ax = rload_df.plot(cmap="RdYlBu")
ax.grid(linestyle="--", lw="0.5")
ax.set_ylabel("Residualload in GW")
# ax.axhline(y=0, color='black', lw=1)
ax.set_xlim(-50, 8860)
ax.set_xlabel("Hour")
plt.savefig("documentation/figures/rload.pdf", bbox_inches="tight")


tuples = {
    (0, 0): ("2050REF-GS-flex0", "2050REF-GS"),
    (0, 1): ("2030DG-flex0", "2030DG"),
    (0, 2): ("2050REF-flex0", "2050REF"),
    (0, 3): ("2040DG-flex0", "2040DG"),
}
fig, axs = plt.subplots(1, 4, sharex=True, sharey=True, figsize=(15, 5))

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
im.columns = im.columns.droplevel(0)

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
ex.columns = ex.columns.droplevel(0)
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
    "documentation/figures/exchange-heat-plot-{}.pdf".format(compare[0]),
    # bbox_extra_artists=(lgd,),
    bbox_inches="tight",
)


# sorted transmission duration ------------------------------------------------
# sorted_exchange = pd.DataFrame(
#     {c: sorted(exchange_df[c].values) for c in exchange_df.columns}
# )
# sorted_exchange.columns = [
#     c.strip("-electricity") for c in sorted_exchange.columns
# ]
# data = sorted_exchange.stack().to_frame()
# data.index.names = ["t", "ctr"]
# data.reset_index(inplace=True)
# sns.set_palette("cubehelix", 11)
# ax = sns.lineplot(x="t", y=0, hue="ctr", data=data)
# ax.grid(linestyle="--", color="gray")
# ax.set_ylabel("Tranmission in GW")
# ax.set_xlabel("Hours")
# lgd = ax.legend(
#     title="",
#     # loc="upper left",
#     bbox_to_anchor=(1.1, 1.3),
#     ncol=4,
#     borderaxespad=0,
#     frameon=False,
# )
# plt.savefig(
#     "documentation/figures/sorted-transmission-DE.pdf",
#     bbox_extra_artists=(lgd,),
#     bbox_inches="tight",
)
