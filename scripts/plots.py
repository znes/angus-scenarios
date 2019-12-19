import os
import pandas as pd

from plotly import tools
import plotly.graph_objs as go
import plotly.offline as offline
from matplotlib import colors

offline.init_notebook_mode()

color = {
    "caes": "brown",
    "air-caes": "brown",
    "gas-ocgt": "gray",
    "gas-ccgt": "lightgray",
    "solar-pv": "gold",
    "wind-onshore": "skyblue",
    "wind-offshore": "darkblue",
    "biomass-st": "olivedrab",
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
    "mixed-st": "darkcyan",
}

color_dict = {name: colors.to_hex(color) for name, color in color.items()}


def filling_level_plot(scenario, datapath="results"):
    """
    """

    df = pd.read_csv(
        os.path.join(datapath, scenario, "output", "filling_levels.csv"),
        index_col=[0],
        parse_dates=True,
    )
    # create plot
    layout = go.Layout(
        barmode="stack",
        title="Filling levels for scenario {}".format(scenario),
        yaxis=dict(
            title="Energy in MWh",
            titlefont=dict(size=16, color="rgb(107, 107, 107)"),
            tickfont=dict(size=14, color="rgb(107, 107, 107)"),
        ),
    )

    data = []
    for storage in [
        "DE-air-caes",
        "DE-lithium-battery",
        "DE-hydro-phs",
        "DE-hydro-rsv",
        "DE-lithium-battery",
    ]:
        data.append(
            go.Scatter(
                x=df.index,
                y=df[storage],
                name=storage,
                # stackgroup="positive",
                line=dict(width=2, color=color_dict.get(storage[3:], "black")),
            )
        )

    return {"data": data, "layout": layout}


def hourly_plot(scenario, bus, datapath="results"):
    """
    """
    df = pd.read_csv(
        os.path.join(
            datapath,
            scenario,
            "output",
            "-".join([bus, "electricity"]) + ".csv",
        ),
        index_col=[0],
        parse_dates=True,
    )

    for i in ["coal", "lignite", "oil", "gas", "waste", "uranium", "mixed"]:
        group = [c for c in df.columns if i in c]
        df[i] = df[group].sum(axis=1)
        df.drop(group, axis=1, inplace=True)

    # df = df.resample('1D').mean()
    x = df.index
    # kind of a hack to get only the technologies
    df.columns = [c.strip(bus + "-") for c in df.columns]

    flexibility = ["import", "caes", "phs", "battery"]

    # create plot
    layout = go.Layout(
        barmode="stack",
        title="Hourly supply and demand in {} for scenario {}".format(
            bus, scenario
        ),
        yaxis=dict(
            title="Energy in MWh",
            titlefont=dict(size=16, color="rgb(107, 107, 107)"),
            tickfont=dict(size=14, color="rgb(107, 107, 107)"),
        ),
    )

    data = []

    for c in df:
        if c in flexibility:
            data.append(
                go.Scatter(
                    x=x,
                    y=df[c].clip(lower=0),
                    name=c,
                    stackgroup="positive",
                    line=dict(width=0, color=color_dict.get(c, "black")),
                )
            )
            if c == "import":
                name = "export"
            else:
                name = c + "-charge"
            data.append(
                go.Scatter(
                    x=x,
                    y=df[c].clip(upper=0),
                    name=name,
                    stackgroup="negative",
                    line=dict(width=0, color=color_dict.get(c, "black")),
                    showlegend=False,
                )
            )

        elif "load" in c:
            # append load
            data.append(
                go.Scatter(
                    x=x, y=df[c], name=c, line=dict(width=3, color="darkred")
                )
            )
        elif "excess" in c:
            pass
        else:
            data.append(
                go.Scatter(
                    x=x,
                    fillcolor=color_dict.get(c, "black"),
                    y=df[c],
                    name=c,
                    stackgroup="positive",
                    line=dict(width=0, color=color_dict.get(c, "black")),
                )
            )

    return {"data": data, "layout": layout}


def stacked_plot(scenario, datapath="results"):
    """
    """
    df = pd.read_csv(
        os.path.join(datapath, scenario, "output", "capacities.csv"),
        index_col=0,
    )

    df = df.groupby(["to", "carrier", "tech"]).sum().unstack("to")
    df.index = ["-".join(i) for i in df.index]

    for i in ["coal", "lignite", "oil", "gas", "waste", "uranium"]:
        group = [c for c in df.index if i in c]
        df.loc[i] = df.loc[group].sum(axis=0)
        df.drop(group, axis=0, inplace=True)

    df.columns = df.columns.droplevel(0)

    return {
        "data": [
            go.Bar(
                x=row.index,
                y=row.values,
                name=idx,
                marker=dict(color=color_dict.get(idx, "black")),
            )
            for idx, row in df.iterrows()
        ],
        "layout": go.Layout(
            barmode="stack",
            title="Installed capacities for scenario {}".format(scenario),
        ),
    }


def price_scatter_plot(scenarios, rload, prices, timestamps, country):
    data = []
    for s in scenarios:
        data.append(
            go.Scatter(
                x=rload[s],
                y=prices[s],
                name=s,
                text=timestamps[s],
                mode="markers",
                marker=dict(size=10),
            )
        )
    layout = dict(
        title="Residual load vs. Shadow Prices {}".format(country),
        yaxis1=dict(title="Shadow price in € / MWh"),
        xaxis=dict(title="Residual load in MW"),
    )

    return dict(data=data, layout=layout)


def merit_order_plot(scenario, prices, storages):
    prices = prices[scenario]
    prices = prices.sort_values(by=["shadow_price"])

    storages = storages[scenario]
    storages = storages.sort_values(by=["shadow_price"])

    prices["colors"] = [color_dict.get(c, "black") for c in prices.carrier]
    # text = [str(t)+' '+str(n) for t in prices.index for n in prices.name]

    fig = tools.make_subplots(rows=2, cols=1)

    data = []

    data.append(
        go.Bar(
            y=prices.shadow_price,
            # text = text,
            opacity=1,
            name="shadow_price",
            showlegend=False,
            width=1.05,
            marker=dict(color=prices.colors),
        )
    )

    fig.append_trace(data[0], 1, 1)

    # just for legend to work
    for c in prices.carrier.unique():
        if c == "NONE":
            fig.append_trace(
                go.Bar(
                    y=[0],
                    # text = text,
                    name="NONE",
                    marker=dict(color=color_dict.get(c, "black")),
                ),
                1,
                1,
            )
        else:
            fig.append_trace(
                go.Bar(
                    y=[0],
                    # text = text,
                    name=c.title(),
                    marker=dict(color=color_dict.get(c, "black")),
                ),
                1,
                1,
            )

    storage_dispatch_ordered = go.Bar(
        y=storages["storage_dispatch"],
        # text = text,
        name="Storage Dispatch",
        width=1.04,
        opacity=1,
        marker=dict(color="magenta"),
    )

    fig.append_trace(storage_dispatch_ordered, 2, 1)

    fig["layout"].update(
        title="Ordered prices and storage dispatch in DE " + scenario,
        yaxis1=dict(title="Shadow price in € / MWh"),
        yaxis2=dict(title="Storage dispatch in MWh"),
        xaxis2=dict(title="Hours of the year"),
        showlegend=True,
        # legend=dict(x=0, y=-0),
        bargap=0,
    )

    return fig


def price_line_plot(scenarios, index, prices, country):
    data = []
    for s in scenarios:
        data.append(
            go.Scatter(x=index, y=prices[s], name=s, line=dict(width=2))
        )
    layout = dict(
        title="Shadow Prices for country {}".format(country),
        yaxis1=dict(title="Shadow price in € / MWh"),
        xaxis=dict(title="Hours of the year"),
    )

    return dict(data=data, layout=layout)
