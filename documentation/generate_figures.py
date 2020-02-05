import os
import pandas as pd
import plotly.io as pio
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
}
color_dict = {name: colors.to_hex(color) for name, color in color.items()}

path = os.path.join(os.getcwd(), "results")

renewables = [
    "hydro-ror",
    "hydro-reservoir",
    "wind-offhsore",
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
]


bus = "DE"
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

total_emissions = (emissions.loc[bus + "-electricity"] / 1e6).round(2)
total_emissions / total_emissions.max()

# re shares -------------------------------------------------------------------
shares = {}
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
        shares[dir] = (re_supply - excess[dir]) / total_supply

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
de = _df / 1000
de.sort_index(axis=1, inplace=True)
ax = (de.T).plot(
    kind="bar", stacked=True, color=[color_dict.get(c) for c in de.index]
)
lgd = ax.legend(loc="upper left", bbox_to_anchor=(1, 1), shadow=True, ncol=1)
ax.set_ylabel("Installed capacity in GW")
ax.grid(linestyle="--")
plt.xticks(rotation=45)
# plt.plot(figsize=(10, 5))
plt.savefig(
    "documentation/figures/installed_capacities.pdf",
    bbox_extra_artists=(lgd,),
    bbox_inches="tight",
)

# energy plot -----------------------------------------------------------------
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

scenarios.loc["storage"] = scenarios.loc[storages].sum()
scenarios.loc["storage-cos"] = scenarios.loc[storages_cos].sum()

scenarios.drop(storages, inplace=True)
scenarios.drop(storages_cos, inplace=True)

scenarios.sort_index(axis=1, inplace=True)


ax = scenarios.T.plot(
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
ax.grid(linestyle="--")
plt.xticks(rotation=45)
# plt.plot(figsize=(10, 5))
plt.savefig(
    "documentation/figures/energy.pdf",
    bbox_extra_artists=(lgd,),
    bbox_inches="tight",
)

offline.plot(
    energy_plot(scenarios, color_dict=color_dict),
    filename=os.path.join(
        interactive_figures, "aggregated_supply_demand.html"
    ),
    auto_open=False,
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


# shadow prices ---------------------------------------------
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
        country_electricity_df = pd.read_csv(data_path, index_col=[0], parse_dates=True)
        country_electricity_df["rload"] = country_electricity_df[
            ("-").join([bus, "electricity-load"])
        ] - country_electricity_df[
            [("-").join([bus, i]) for i in renewables]
        ].sum(
            axis=1
        )

        rload[dir] = country_electricity_df["rload"].values
        timestamps[dir] = country_electricity_df.index


for k in rload.keys():
    ax = plt.scatter(rload[k]/1e3, unsorted[k], s=1, marker='o', label=k)
plt.ylabel("Residual load in GW")
plt.xlabel("Shadow price in Euro / MWh")
plt.grid(linestyle="--", color="lightgray")
plt.title('Shadow prices vs. Residual load')
plt.legend(loc=2)
plt.savefig(
    "documentation/figures/shadow-prices-vs-rload.pdf",
    bbox_extra_artists=(lgd,),
    bbox_inches="tight",
)
