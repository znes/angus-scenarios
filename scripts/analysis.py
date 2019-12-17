import os
import pandas as pd
import matplotlib.pyplot as plt
import datapackage as dp
import plotly.io as pio
import plotly.offline as offline

from plots import (
    hourly_plot,
    stacked_plot,
    price_line_plot,
    price_scatter_plot,
    merit_order_plot,
    filling_level_plot,
)

results = [r for r in os.listdir("results") if "plots" not in r]


country = "DE"

# shadow prices
sorted = {}
unsorted = {}
for r in results:
    path = os.path.join("results", r, "output", "shadow_prices.csv")
    sprices = pd.read_csv(path, index_col=[0], parse_dates=True)[
        country + "-electricity"
    ]
    sorted[r] = sprices.sort_values().values
    unsorted[r] = sprices.values


# residual load and more
renewables = ["wind-onshore", "wind-offshore", "solar-pv", "hydro-ror"]
timestamps = {}

marginal_cost = {}
shadow_prices = {}
storages = {}
prices = {}
rload = {}
for r in results:

    path = os.path.join("results", r, "output", country + "-electricity.csv")
    country_electricity_df = pd.read_csv(path, index_col=[0], parse_dates=True)
    country_electricity_df["rload"] = country_electricity_df[
        ("-").join([country, "electricity-load"])
    ] - country_electricity_df[
        [("-").join([country, i]) for i in renewables]
    ].sum(
        axis=1
    )

    rload[r] = country_electricity_df["rload"].values
    timestamps[r] = country_electricity_df.index

    if country == "DE":

        path = os.path.join("results", r, "input", "datapackage.json")
        input_datapackage = dp.Package(path)
        dispatchable = input_datapackage.get_resource("dispatchable")
        df = pd.DataFrame(dispatchable.read(keyed=True))
        df = df.set_index("name")
        # select all storages and sum up
        storage = [
            ss
            for ss in [
                "DE-" + s for s in ["hydro-phs", "hydro-reservoir", "battery"]
            ]
            if ss in country_electricity_df.columns
        ]
        storages[r] = country_electricity_df[storage].sum(axis=1)

        marginal_cost[r] = df

        path = os.path.join("results", r, "output", "shadow_prices.csv")
        shadow_prices[r] = pd.read_csv(path, index_col=[0], parse_dates=True)[
            "DE-electricity"
        ]

        storages[r] = pd.concat([storages[r], shadow_prices[r]], axis=1)
        storages[r] = storages[r].rename(
            columns={0: "storage_dispatch", "DE-electricity": "shadow_price"}
        )

        prices[r] = []
        for c in country_electricity_df.iterrows():
            timestamp = c[0]
            energy = c[1]
            energy.name = "energy"
            df = pd.concat([c[1], marginal_cost[r]], axis=1, sort=False)
            df = df.dropna()
            df = df[df["energy"] > 0]
            df = df.sort_values(by="marginal_cost", ascending=False)
            if df.shape[0] > 1:
                df_carrier = df.carrier[0]
                df_marginal_cost = df.marginal_cost[0]
                df_name = df.index[0]
            else:
                df_carrier = "NONE"
                df_marginal_cost = -1
                df_name = "NONE"
            temp_dict = dict(
                timestamp=timestamp,
                carrier=df_carrier,
                name=df_name,
                marginal_cost=df_marginal_cost,
                shadow_price=shadow_prices[r][timestamp],
            )
            prices[r].append(temp_dict)

prices = {r: pd.DataFrame(prices[r]).set_index("timestamp") for r in prices}


if not os.path.exists("results/plots"):
    os.makedirs("results/plots")

# plot for all scenarios
offline.plot(
    price_line_plot(results, sprices.index, unsorted, country),
    filename=os.path.join("results", "plots", "shadow-prices.html"),
    auto_open=False,
)

offline.plot(
    price_scatter_plot(results, rload, unsorted, timestamps, country),
    filename=os.path.join(
        "results", "plots", "shadow_prices-vs-residual_load.html"
    ),
    auto_open=False,
)


for s in results:
    scenario_plots = os.path.join("results", "plots", s)
    if not os.path.exists(scenario_plots):
        os.makedirs(scenario_plots)

    offline.plot(
        filling_level_plot(s),
        filename=os.path.join(scenario_plots, s + "-filling-levels.html"),
        auto_open=False,
    )

    offline.plot(
        stacked_plot(s),
        filename=os.path.join(scenario_plots, s + "-capacities.html"),
        auto_open=False,
    )
    offline.plot(
        hourly_plot(s, "DE"),
        filename=os.path.join(scenario_plots, s + "-dispatch.html"),
        auto_open=False,
    )

    if country == "DE":
        offline.plot(
            merit_order_plot(s, prices, storages),
            filename=os.path.join(
                scenario_plots, "merit-order-" + s + ".html"
            ),
            auto_open=False,
        )

        # pio.write_image(
        #     merit_order_plot(s, prices, storages),
        #     os.path.join(scenario_plots, 'merit_order_' + s +'.pdf'))
