import os
import pandas as pd

from plotly import tools
import plotly.graph_objs as go
import plotly.offline as offline
from matplotlib import colors

offline.init_notebook_mode()

color = {
    "acaes": "brown",
    "cavern-acaes": "brown",
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
    "hydrogen-storage": "skyblue",
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
