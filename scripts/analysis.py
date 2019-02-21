import os
import pandas as pd
import matplotlib.pyplot as plt

country = 'DK'

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


# residual load
renewables = ['wind-onshore', 'wind-offshore', "solar-pv", "hydro-ror"]

if country == 'DE':
    rload = {}
    for r in os.listdir("results"):
        path = os.path.join("results", r, "output", country + "-electricity.csv")
        df = pd.read_csv(path, index_col=[0], parse_dates=True)

        df['rload'] = (
            df[("-").join([country, 'electricity-load'])] -
            df[[("-").join([country, i]) for i in renewables]].sum(axis=1)
        )

        rload[r] = df['rload'].values

from plots import hourly_plot, stacked_plot, price_line_plot
import plotly.offline as offline

if not os.path.exists('plots'):
    os.makedirs('plots')

for s in os.listdir('results'):
    offline.plot(
        stacked_plot(s), filename=os.path.join('plots', s + '-capacities'))
    offline.plot(
        hourly_plot(s, 'DE'), filename=os.path.join('plots', s + '-dispatch'))

offline.plot(
          price_line_plot(os.listdir('results'), s.index, unsorted),
          filename=os.path.join('plots', 'shadow_prices'))
