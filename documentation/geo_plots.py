# -*- coding: utf-8 -*-
"""
"""
import os
from datapackage import Package
import geopandas as gpd
import pandas as pd
import plotly.graph_objs as go
from shapely.geometry import LineString
from shapely import wkt
import pycountry


scenario = "ANGUS2050"

p = Package(os.path.join("datapackages", scenario, "datapackage.json"))

regions = gpd.GeoDataFrame(p.get_resource("buses").read(keyed=True)).set_index(
    "name"
)

regions["geometry"] = regions["geometry"].apply(wkt.loads)

conns = pd.DataFrame(p.get_resource("link").read(keyed=True)).set_index("name")

demand = pd.DataFrame(p.get_resource("load").read(keyed=True)).set_index(
    "name"
)

conns_geo = conns.copy()

conns_geo["geometry"] = conns_geo.apply(
    lambda r: LineString(
        [
            regions.loc[r["from_bus"], "geometry"].centroid,
            regions.loc[r["to_bus"], "geometry"].centroid,
        ]
    ),
    axis=1,
)


layout = go.Layout(
    title="Transmission capacities in scenario {}".format(scenario),
    geo=dict(
        resolution=50,
        showframe=False,
        scope="europe",
        showcoastlines=True,
        showland=True,
        landcolor="rgb(229, 229, 229)",
        countrycolor="rgb(255, 255, 255)",
        coastlinecolor="rgb(255, 255, 255)",
        projection=dict(type="mercator"),
        lonaxis=dict(range=[-5, 25]),
        lataxis=dict(range=[42, 68]),
        domain=dict(x=[0, 1], y=[0, 1]),
    ),
    width=800,
    height=1200,
    margin=dict(l=20, r=20, t=30, b=20),
)


lines = [
    go.Scattergeo(
        lon=tuple(row.geometry.xy[0]),
        lat=tuple(row.geometry.xy[1]),
        hoverinfo="skip",
        name=ix,
        showlegend=False,
        line_color="lightgray",
        line={"width": row.from_to_capacity / 1000, "color": "darkgray"},
        mode="lines",
    )
    for ix, row in conns_geo.iterrows()
]

# # for hover infor on mid one lines
# mid_edge_trace = [
#     go.Scattergeo(
#         lon=[row.geometry.centroid.xy[0][0]],
#         lat=[row.geometry.centroid.xy[1][0]],
#         text="Line " + ix + " has capacity %.1f MW" % row.from_to_capacity,
#         mode="markers",
#         hoverinfo='text',
#         showlegend=False,
#         opacity=0)
#     for ix, row in conns_geo.iterrows()]

capacities = [
    go.Scattergeo(
        lon=[row.geometry.centroid.xy[0][0]],
        lat=[row.geometry.centroid.xy[1][0]],
        text=str(row.from_to_capacity / 1000) + " GW",
        mode="text",
        textfont={"size": 12, "color": "darkred"},
        showlegend=False,
        opacity=1,
    )
    for ix, row in conns_geo.iterrows()
]

demand_color = [
    go.Choropleth(
        locations=[
            pycountry.countries.get(alpha_2=r[0:2]).alpha_3
            for r in demand.index
        ],
        z=demand.amount.astype(float) / 1e6,
        text="",
        colorscale="YlGnBu",
        autocolorscale=False,
        reversescale=False,
        marker_line_color="lightgray",
        marker_line_width=0.5,
        colorbar_tickprefix="",
        colorbar_title="Demand in TWh",
    )
]

names = [
    go.Scattergeo(
        lon=[row.geometry.centroid.xy[0][0]],
        lat=[row.geometry.centroid.xy[1][0]],
        text=[ix[0:2]],
        textfont={"size": 18, "color": "gray"},
        mode="text",
        showlegend=False,
    )
    for ix, row in regions.iterrows()
]

fig = go.Figure(layout=layout, data=lines + names + capacities + demand_color)

fig.write_image(
    os.path.join("documentation", "grid-scenario" + scenario + ".pdf")
)
# off.iplot(fig, filename='e-highway-transshipment-capacities.html')
