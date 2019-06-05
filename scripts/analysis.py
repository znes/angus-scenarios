import os
import pandas as pd
import matplotlib.pyplot as plt
import datapackage as dp

country = 'DE'

# shadow prices
sorted = {}
unsorted = {}
for r in os.listdir("results"):
    path = os.path.join("results", r, "output", "shadow_prices.csv")
    s = pd.read_csv(path, index_col=[0], parse_dates=True)["DE-electricity"]
    sorted[r] = s.sort_values().values
    unsorted[r] = s.values

#pd.DataFrame(sorted).to_csv("results/shadow_prices_sorted.csv")
#pd.DataFrame(unsorted).to_csv("results/shadow_prices_unsorted.csv")


# residual load and more
renewables = ['wind-onshore', 'wind-offshore', "solar-pv", "hydro-ror"]
timestamps = {}
if country == 'DE':
    rload = {}
    marginal_cost = {}
    shadow_prices = {}
    storages = {}
    prices = {}
    for r in os.listdir("results"):
        path = os.path.join("results", r, "output", country + "-electricity.csv")
        country_electricity_df = pd.read_csv(path, index_col=[0], parse_dates=True)
        country_electricity_df['rload'] = (
            country_electricity_df[("-").join([country, 'electricity-load'])] -
            country_electricity_df[[("-").join([country, i]) for i in renewables]].sum(axis=1)
        )

        rload[r] = country_electricity_df['rload'].values
        timestamps[r] = country_electricity_df.index

        path = os.path.join("results", r, "input", "datapackage.json")
        input_datapackage = dp.Package(path)
        dispatchable = input_datapackage.get_resource('dispatchable')
        df = pd.DataFrame(dispatchable.read(keyed=True))
        df = df.set_index('name')
        # select all storages and sum up
        storage = [ss for ss in
                    ['DE-' + s for s in ['hydro-phs', 'hydro-reservoir', 'battery']]
                    if ss in country_electricity_df.columns]
        storages[r] = country_electricity_df[storage].sum(axis=1)

        marginal_cost[r] = df

        path = os.path.join("results", r, "output", "shadow_prices.csv")
        shadow_prices[r] = pd.read_csv(path, index_col=[0], parse_dates=True)["DE-electricity"]

        storages[r] = pd.concat([storages[r], shadow_prices[r]], axis=1)
        storages[r] = storages[r].rename(
            columns={0:'storage_dispatch', 'DE-electricity': 'shadow_price'})

        prices[r] =[]
        for c in country_electricity_df.iterrows():
            timestamp = c[0]
            energy = c[1]
            energy.name = 'energy'
            df = pd.concat([c[1], marginal_cost[r]], axis=1, sort=False)
            df = df.dropna()
            df = df[df['energy']>0]
            df = df.sort_values(by='marginal_cost', ascending=False)
            if df.shape[0] > 1:
                df_carrier = df.carrier[0]
                df_marginal_cost = df.marginal_cost[0]
                df_name = df.index[0]
            else:
                df_carrier = 'NONE'
                df_marginal_cost = -1
                df_name = 'NONE'
            temp_dict = dict(timestamp = timestamp,
                             carrier = df_carrier,
                             name = df_name,
                             marginal_cost = df_marginal_cost,
                             shadow_price = shadow_prices[r][timestamp])
            prices[r].append(temp_dict)
        prices[r] = pd.DataFrame(prices[r]).set_index('timestamp')

from plots import hourly_plot, stacked_plot, price_line_plot, price_scatter_plot, merit_order_plot
import plotly.offline as offline

if not os.path.exists('plots'):
    os.makedirs('plots')
#
if False:
    for s in os.listdir('results'):
        offline.plot(
            stacked_plot(s), filename=os.path.join('plots', s + '-capacities'))
        offline.plot(
            hourly_plot(s, 'DE'), filename=os.path.join('plots', s + '-dispatch'))

#offline.plot(
#          price_line_plot(os.listdir('results'), s.index, unsorted),
#          filename=os.path.join('plots', 'shadow_prices'))


# offline.plot(
#           price_scatter_plot(os.listdir('results'), rload, unsorted, timestamps),
#           filename=os.path.join('plots', 'shadow_prices'))

for s in os.listdir('results'):
    offline.plot(
        merit_order_plot(s, prices, storages),
        filename = os.path.join('plots', 'merit_order_'+s+'.html'),
        auto_open = False)
