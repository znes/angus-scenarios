import os
import pandas as pd

import plotly.graph_objs as go
import plotly.offline as offline
from matplotlib import colors

offline.init_notebook_mode()

color = {
    'acaes': 'brown',
    'gas-ocgt': 'gray',
    'gas-ccgt': 'lightgray',
    'solar-pv': 'gold',
    'wind-onshore': 'skyblue',
    'wind-offshore': 'darkblue',
    'biomass-ce': 'olivedrab',
    'battery': 'lightsalmon',
    'electricity': 'lightsalmon',
    'hydro-ror': 'aqua',
    'hydro-phs': 'darkred',
    'hydro-reservoir': 'magenta',
    'biomass': 'olivedrab',
    'uranium': 'yellow',
    'hydro': 'aqua',
    'wind': 'skyblue',
    'solar': 'gold',
    'gas': 'lightgray',
    'lignite': "chocolate",
    'coal': "darkgray",
    'waste': 'yellowgreen',
    'oil': 'black',
    'import': 'pink',
}

color_dict = {
    name: colors.to_hex(color) for name, color in color.items()}

def hourly_plot(scenario, bus, datapath='results'):
    """
    """
    df = pd.read_csv(
        os.path.join(
            datapath,
            scenario,
            'output',
            '-'.join([bus, 'electricity']) + '.csv'),
        index_col=[0], parse_dates=True)


    for i in ['coal', 'lignite', 'oil', 'gas', 'waste', 'uranium']:
        group = [c for c in df.columns if i in c]
        df[i] = df[group].sum(axis=1)
        df.drop(group, axis=1, inplace=True)

    #df = df.resample('1D').mean()
    x = df.index
    # kind of a hack to get only the technologies
    df.columns = [c.strip(bus + '-') for c in df.columns]

    flexibility = ['import', 'acaes', 'phs', 'lithium_battery', 'battery']

    # create plot
    layout = go.Layout(
        barmode='stack',
        title='Hourly supply and demand in {} for scenario {}'.format(bus, scenario),
        yaxis=dict(
            title='Energy in MWh',
            titlefont=dict(
                size=16,
                color='rgb(107, 107, 107)'
            ),
            tickfont=dict(
                size=14,
                color='rgb(107, 107, 107)'
            )
        )
    )

    data = []

    for c in df:
        if c in flexibility:
            data.append(
                go.Scatter(
                    x = x,
                    y = df[c].clip(lower=0),
                    name=c,
                    stackgroup='positive',
                    line=dict(width=0, color=color_dict.get(c, 'black'))
                )
            )
            data.append(
                go.Scatter(
                    x = x,
                            y = df[c].clip(upper=0),
                    name=c+'-charge',
                    stackgroup='negative',
                    line=dict(width=0, color=color_dict.get(c, 'black')),
                    showlegend= False
                )
            )

        elif 'load' in c:
            # append load
            data.append(
                go.Scatter(
                    x = x,
                    y = df[c],
                    name = c,
                    line=dict(width=3, color='darkred')
                )
            )
        elif 'excess' in c:
            pass
        else:
            data.append(
                go.Scatter(
                    x = x,
                    fillcolor = color_dict.get(c, 'black'),
                    y = df[c],
                    name=c,
                    stackgroup='positive',
                    line=dict(width=0, color=color_dict.get(c, 'black'))
                )
            )

    return {'data': data, 'layout': layout}

def stacked_plot(scenario, datapath='results'):
    """
    """
    df = pd.read_csv(
        os.path.join(datapath, scenario, 'output', 'capacities.csv'),
        index_col=0)

    df = df.groupby(['to', 'carrier', 'tech']).sum().unstack('to')
    df.index = ['-'.join(i) for i in df.index]

    for i in ['coal', 'lignite', 'oil', 'gas', 'waste', 'uranium']:
        group = [c for c in df.index if i in c]
        df.loc[i] = df.loc[group].sum(axis=0)
        df.drop(group, axis=0, inplace=True)

    df.columns = df.columns.droplevel(0)


    return {
        'data': [go.Bar(
            x = row.index,
            y = row.values,
            name = idx,
            marker=dict(color=color_dict.get(idx, 'black'))
       ) for idx, row in df.iterrows()],
       'layout': go.Layout(
            barmode='stack',
            title="Installed capacities for scenario {}".format(scenario)
       )
    }

def price_scatter_plot(scenarios, rload, prices):
    data = []
    for s in scenarios:
        data.append(
            go.Scatter(
                x = rload[s],
                y = prices[s],
                name = s,
                mode = 'markers',
                marker = dict(
                    size = 10,
                )
            )
        )
    layout = dict(title = 'Residual load vs. Shadow Prices')

    return dict(data=data, layout=layout)

def merit_order_plot(scenario, rload, prices):
    data = []
    data.append(
        go.Scatter(
            x = rload[scenario],
            y = prices[scenario],
            name = scenario,
            mode = 'markers',
            marker = dict(
                size = 10,
            )
        )
    )
    layout = dict(title = 'Residual load vs. Shadow Prices')

    return dict(data=data, layout=layout)

def price_line_plot(scenarios, index, prices):
    data = []
    for s in scenarios:
        data.append(
            go.Scatter(
                x = index,
                y = prices[s],
                name=s,
                line=dict(width=2)
            )
        )
    layout = dict(title = 'Shadow Prices')

    return dict(data=data, layout=layout)
