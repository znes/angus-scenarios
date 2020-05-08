import plotly.graph_objs as go


def hourly_plot(df, scenario, bus, color_dict, conventionals, storages):
    """
    """

    for i in conventionals:
        carrier = i.split("-")[0]
        group = [c for c in df.columns if carrier in c]
        df[i] = df[group].sum(axis=1)
        df.drop(group, axis=1, inplace=True)

    # df = df.resample('1D').mean()
    x = df.index
    # kind of a hack to get only the technologies
    df.columns = [c.strip(bus + "-") for c in df.columns]

    flexibility = ["import"]
    dload = ["decentral_heat-gshp", "flex-decentral_heat-gshp"]

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
        if df[c].sum() != 0:
            if c in flexibility or c in storages:
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

            elif c in dload:
                data.append(
                    go.Scatter(
                        x=x,
                        y=df[c] * -1,
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
                        x=x,
                        y=df[c],
                        name=c,
                        line=dict(width=3, color=color_dict.get(c)),
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


def filling_level_plot(
    df,
    scenario,
    bus="DE",
    storages=[
        "cavern-acaes",
        "lithium-battery",
        "hydro-phs",
        "redox-battery",
        "hydro-reservoir",
        "hydrogen-storage",
    ],
    color_dict={},
):
    """
    """
    storages = [bus + "-" + s for s in storages]

    # create plot
    layout = go.Layout(
        barmode="stack",
        title="Filling levels for scenario {}".format(scenario),
        yaxis=dict(
            title="Energy in GWh",
            titlefont=dict(size=16, color="rgb(107, 107, 107)"),
            tickfont=dict(size=14, color="rgb(107, 107, 107)"),
        ),
    )

    data = []
    for storage in storages:
        if storage in df.columns:
            data.append(
                go.Scatter(
                    x=df.index,
                    y=df[storage] / 1000,  # GWh
                    name=storage,
                    # stackgroup="positive",
                    line=dict(
                        width=2, color=color_dict.get(storage[3:], "black")
                    ),
                )
            )

    return {"data": data, "layout": layout}


def stacked_plot(df, scenario, color_dict):
    """
    """

    # for i in ["coal", "lignite", "oil", "gas", "waste", "uranium"]:
    #     group = [c for c in df.index if i in c]
    #     df.loc[i] = df.loc[group].sum(axis=0)
    #     df.drop(group, axis=0, inplace=True)

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
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis={"gridcolor": "black", "linecolor": "lightgray"},
        ),
    }


def energy_plot(scenarios, color_dict):
    """
    """
    layout = go.Layout(
        barmode="relative",
        legend_orientation="h",
        title="Aggregated supply and demand",
        # width=400,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(
            title="Energy in {}".format("TWh"),
            titlefont=dict(size=16, color="rgb(107, 107, 107)"),
            tickfont=dict(size=14, color="rgb(107, 107, 107)"),
        ),
    )

    data = []
    for idx, row in scenarios.T.iteritems():

        if "-cos" in idx:
            legend = False
        else:
            legend = True
        data.append(
            go.Bar(
                x=row.index,
                y=row.values,
                text=[
                    v.round(1) if v > 20 or v < -20 else None
                    for v in row.values
                ],
                hovertext=[
                    ", ".join([str(v.round(2)), idx.replace("-cos", "")])
                    for v in row.values
                ],
                hoverinfo="text",
                textposition="auto",
                showlegend=legend,
                name=idx,
                marker=dict(
                    color=color_dict.get(idx.replace("-cos", ""), "gray")
                ),
            )
        )

    return {"data": data, "layout": layout}
