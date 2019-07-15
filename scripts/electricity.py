# -*- coding: utf-8 -*-
"""
"""
import json
import os

from datapackage import Package
from decimal import Decimal

import pandas as pd
import numpy as np

from oemof.tabular.datapackage import building



def tyndp_generation(buses, avf, vision, scenario_year, scenario,
                     efficiencies, max_fulloadhours,
                     datapackage_dir, raw_data_path):
    """

    """

    filepath = building.download_data(
        "https://www.entsoe.eu/Documents/TYNDP%20documents/TYNDP%202016/rgips/"
        "TYNDP2016%20market%20modelling%20data.xlsx",
        directory=raw_data_path)
    df = pd.read_excel(filepath, sheet_name="NGC")


    visions = {
        'vision1': 41,
        'vision2': 80,
        'vision3': 119,
        'vision4': 158
     }
    # 41:77 for 2030 vision 1
    # 80:116 for 2030 vision 2 or from ehighway scenario?
    # ....
    x = df.iloc[
        visions[vision]: visions[vision] + 36
    ]
    x.columns = x.iloc[0,:]
    x.drop(x.index[0], inplace=True)
    x.rename(columns={
        x.columns[0]: 'country',
        'Hard coal': 'coal',
        'Nuclear': 'uranium'},
             inplace=True)
    x.set_index('country', inplace=True)
    x.dropna(axis=1, how='all', inplace=True) # drop unwanted cols
    x['biomass'] = x['Biofuels'] + x['Others RES']
    x.drop(['Biofuels', 'Others RES'], axis=1, inplace=True)
    x.columns = [i.lower().replace(' ', '-') for i in x.columns]

    carriers = pd.DataFrame(
        Package('https://raw.githubusercontent.com/ZNES-datapackages/technology-cost/master/datapackage.json')
        .get_resource('carrier').read(keyed=True)).set_index(
            ['year', 'carrier', 'parameter', 'scenario']).sort_index()

    elements = {}

    for b in buses:
        for carrier in x.columns:
            element = {}

            if carrier in ['wind', 'solar']:
                if "wind" in carrier:
                    profile = b + "-onshore-profile"
                    tech = 'onshore'
                elif "solar" in carrier:
                    profile = b + "-pv-profile"
                    tech = 'pv'

                elements['-'.join([b, carrier, tech])] = element
                e = {
                    "bus": b + "-electricity",
                    "tech": tech,
                    "carrier": carrier,
                    "capacity": x.at[b, carrier],
                    "type": "volatile",
                    "profile": profile,
                }

                element.update(e)

            elif carrier in ['gas', 'coal', 'lignite', 'oil', 'uranium']:
                if carrier == 'gas':
                    tech = 'gt'
                else:
                    tech = 'st'
                elements['-'.join([b, carrier, tech])] = element
                marginal_cost = float(
                    carriers.at[(scenario_year, carrier, 'cost', scenario), 'value']
                    + carriers.at[(2014, carrier, 'emission-factor', None), 'value']
                    * carriers.at[(scenario_year, 'co2', 'cost', scenario), 'value']
                ) / efficiencies[carrier]

                element.update({
                    "carrier": carrier,
                    "capacity": x.at[b, carrier],
                    "bus": b + "-electricity",
                    "type": "dispatchable",
                    "marginal_cost": marginal_cost,
                    "profile": avf[carrier],
                    "tech": tech,
                    "output_parameters": json.dumps({})
                }
            )

            elif carrier == 'others-non-res':
                elements[b + "-" + carrier] = element

                element.update({
                    "carrier": 'other',
                    "capacity": x.at[b, carrier],
                    "bus": b + "-electricity",
                    "type": "dispatchable",
                    "marginal_cost": 0,
                    "tech": 'other',
                    "profile": 1,
                    "output_parameters": json.dumps(
                        {"summed_max": max_fulloadhours['other_non_renewables']}
                    )
                }
            )

            elif carrier == "biomass":
                elements["-".join([b, carrier, 'ce'])] = element

                element.update({
                    "carrier": carrier,
                    "capacity": x.at[b, carrier],
                    "to_bus": b + "-electricity",
                    "efficiency": efficiencies[carrier],
                    "from_bus": b + "-biomass-bus",
                    "type": "conversion",
                    "carrier_cost": float(
                        carriers.at[(2030, carrier, 'cost', scenario), 'value']
                    ),
                    "tech": 'ce',
                    }
                )

    df = pd.DataFrame.from_dict(elements, orient="index")
    df = df[df.capacity != 0]

    # write elements to CSV-files
    for element_type in ['dispatchable', 'volatile', 'conversion']:
        building.write_elements(
            element_type + ".csv",
            df.loc[df["type"] == element_type].dropna(how="all", axis=1),
            directory=os.path.join(datapackage_dir, "data", "elements"),
        )




def DE_nep_conventional(year, datapackage_dir, scenario, bins, avf,
                     max_fulloadhours, cost_scenario, raw_data_path=None):
    """
    """

    technologies = pd.DataFrame(
        #Package('/home/planet/data/datapackages/technology-cost/datapackage.json')
        Package('https://raw.githubusercontent.com/ZNES-datapackages/technology-cost/master/datapackage.json')
        .get_resource('electricity').read(keyed=True)).set_index(
            ['year', 'carrier', 'tech', 'parameter'])

    carriers = pd.DataFrame(
        #Package('/home/planet/data/datapackages/technology-cost/datapackage.json')
        Package('https://raw.githubusercontent.com/ZNES-datapackages/technology-cost/master/datapackage.json')
        .get_resource('carrier').read(keyed=True)).set_index(
            ['year', 'carrier', 'parameter', 'scenario', 'unit']).sort_index()

    sq = pd.read_csv(building.download_data(
        "https://data.open-power-system-data.org/conventional_power_plants/"
        "2018-12-20/conventional_power_plants_DE.csv",
        directory=raw_data_path)
        , encoding='utf-8')

    sq.set_index("id", inplace=True)

    nep = pd.read_excel(building.download_data(
        "https://www.netzentwicklungsplan.de/sites/default/files/"
        "paragraphs-files/Kraftwerksliste_%C3%9CNB_Entwurf_Szenariorahmen_2030_V2019.xlsx",
        directory=raw_data_path)
        , encoding='utf-8')

    pp = nep.loc[nep["Nettonennleistung " + scenario + " [MW]"] != 0]["BNetzA-ID"]
    pp = list(set([i for i in pp.values if  not pd.isnull(i)]))
    df = sq.loc[pp]

    cond1 = df['country_code'] == 'DE'
    cond2 = df['fuel'].isin(['Hydro'])
    cond3 = (df['fuel'] == 'Other fuels') & (df['technology'] == 'Storage technologies')

    df = df.loc[cond1 & ~cond2 & ~cond3, :].copy()

    mapper = {('Biomass and biogas', 'Steam turbine'): ('biomass', 'st'),
              ('Biomass and biogas', 'Combustion Engine'): ('biomass', 'ce'),
              ('Hard coal', 'Steam turbine'): ('coal', 'st'),
              ('Hard coal', 'Combined cycle'): ('coal', 'ccgt'),
              ('Lignite', 'Steam turbine'): ('lignite', 'st'),
              ('Natural gas', 'Gas turbine'): ('gas', 'ocgt'),
              ('Natural gas', 'Steam turbine'): ('gas', 'st'),
              ('Natural gas', 'Combined cycle'): ('gas', 'ccgt'),
              ('Natural gas', 'Combustion Engine'): ('gas', 'st'),  # other technology
              ('Nuclear', 'Steam turbine'): ('uranium', 'st'),
              ('Oil', 'Steam turbine'): ('oil', 'st'),
              ('Oil', 'Gas turbine'): ('oil', 'st'),
              ('Oil', 'Combined cycle'): ('oil', 'st'),
              ('Other fuels', 'Steam turbine'): ('waste', 'chp'),
              ('Other fuels', 'Combined cycle'): ('gas', 'ccgt'),
              ('Other fuels', 'Gas turbine'): ('gas', 'ocgt'),
              ('Waste', 'Steam turbine'): ('waste', 'chp'),
              ('Waste', 'Combined cycle'): ('waste', 'chp'),
              ('Other fossil fuels', 'Steam turbine'): ('coal', 'st'),
              ('Other fossil fuels', 'Combustion Engine'): ('gas', 'st'),
              ('Mixed fossil fuels', 'Steam turbine'): ('gas', 'st')}

    df['carrier'], df['tech'] = zip(*[mapper[tuple(i)] for i in df[['fuel', 'technology']].values])

    etas = df.groupby(['carrier', 'tech']).mean()['efficiency_estimate'].to_dict()
    index = df['efficiency_estimate'].isna()
    df.loc[index, 'efficiency_estimate'] = \
        [etas[tuple(i)] for i in df.loc[index, ('carrier', 'tech')].values]

    index = df['carrier'].isin(['gas', 'coal', 'lignite'])

    df.loc[index, 'bins'] = df[index].groupby(['carrier', 'tech'])['capacity_net_bnetza']\
        .apply(lambda i: pd.qcut(i, bins, labels=False, duplicates='drop'))

    df['bins'].fillna(0, inplace=True)

    s = df.groupby(['country_code', 'carrier', 'tech', 'bins']).\
        agg({'capacity_net_bnetza': sum, 'efficiency_estimate': np.mean})

    elements = {}

    co2 = carriers.at[(year, 'co2', 'cost', cost_scenario, 'EUR/t'), 'value']

    for (country, carrier, tech, bins), (capacity, eta) in s.iterrows():
        name = country + '-' + carrier + '-' + tech + '-' + str(bins)

        vom = technologies.at[(year, carrier, tech, 'vom'), 'value']
        ef = carriers.at[(2015, carrier, 'emission-factor', None, 't (CO2)/MWh'), 'value']
        fuel = carriers.at[(year, carrier, 'cost', '2030ST', 'EUR/MWh'), 'value']

        marginal_cost = (fuel + vom + co2 * ef) / Decimal(eta)

        output_parameters = {}

        if carrier == "waste":
            output_parameters.update(
                {"summed_max": max_fulloadhours["waste"]})

        element = {
            'bus': country + '-electricity',
            'tech': tech,
            'carrier': carrier,
            'capacity': capacity,
            'marginal_cost': float(marginal_cost),
            "profile": avf,
            'output_parameters': json.dumps(output_parameters),
            'type': 'dispatchable'}

        elements[name] = element


    building.write_elements(
        'dispatchable.csv',
        pd.DataFrame.from_dict(elements, orient='index'),
        directory=os.path.join(datapackage_dir, 'data', 'elements'))

def DE_nep(datapackage_dir, raw_data_path, nep_scenario, efficiencies):
    """
    """
    data = pd.read_csv(
            os.path.join(raw_data_path, 'nep2019_data.csv'), index_col=0 )

    carriers = pd.DataFrame(
        #Package('/home/planet/data/datapackages/technology-cost/datapackage.json')
        Package('https://raw.githubusercontent.com/ZNES-datapackages/technology-cost/master/datapackage.json')
        .get_resource('carrier').read(keyed=True)).set_index(
            ['year', 'carrier', 'parameter', 'scenario', 'unit']).sort_index()
    # add renewables
    elements =  {}

    b = 'DE'
    for carrier, tech in [('wind', 'offshore'), ('wind', 'onshore'),
            ('solar', 'pv'), ('biomass', 'ce')]:
        element = {}
        if carrier in ['wind', 'solar']:
            if "onshore" == tech:
                profile = b + "-onshore-profile"
                capacity = data.loc[nep_scenario, "onshore"]
            elif "offshore" == tech:
                profile = b + "-offshore-profile"
                capacity = data.loc[nep_scenario, "offshore"]
            elif "pv" in tech:
                profile = b + "-pv-profile"
                capacity = data.loc[nep_scenario, "pv"]

            elements["-".join([b, carrier, tech])] = element
            e = {
                "bus": b + "-electricity",
                "tech": tech,
                "carrier": carrier,
                "capacity": capacity,
                "type": "volatile",
                "profile": profile,
            }

            element.update(e)


        elif carrier == "biomass":
            elements["-".join([b, carrier, tech])] = element

            element.update({
                "carrier": carrier,
                "capacity": data.loc[nep_scenario, "biomass"],
                "to_bus": b + "-electricity",
                "efficiency": efficiencies['biomass'],
                "from_bus": b + "-biomass-bus",
                "type": "conversion",
                "carrier_cost": float(
                    carriers.at[(2030, carrier, 'cost', '2030ST'), 'value']
                ),
                "tech": 'ce',
                }
            )

    elements['DE-battery'] =    {
            "storage_capacity": 5 * data.loc[nep_scenario, "battery"],  # 5 h
            "capacity": data.loc[nep_scenario, "battery"],
            "bus": "DE-electricity",
            "tech": 'battery',
            "carrier": 'electricity',
            "type": "storage",
            "efficiency": efficiencies['battery']** 0.5,  # convert roundtrip to input / output efficiency
            "marginal_cost": 0.0000001,
            "loss": 0.01
        }

    load = building.read_elements(
        "load.csv",
        directory=os.path.join(datapackage_dir, "data", "elements"))

    load.loc['DE-electricity-load', 'amount'] = data.loc[nep_scenario, "demand"]

    df = pd.DataFrame.from_dict(elements, orient="index")

    for element_type in ['volatile', 'conversion', 'storage', 'load']:
        building.write_elements(
            element_type + ".csv",
            df.loc[df["type"] == element_type].dropna(how="all", axis=1),
            directory=os.path.join(datapackage_dir, "data", "elements"),
        )

def ehighway_generation(
        buses, avf, efficiencies, scenario_year, datapackage_dir,
        scenario="100% RES", raw_data_path=None):
    """
    """

    scenario_mapper = {
        "100% RES": 'T54'}

    filename = 'e-Highway_database_per_country-08022016.xlsx'

    df = pd.read_excel(building.download_data(
        'http://www.e-highway2050.eu/fileadmin/documents/Results/'  +
        filename,
        directory=raw_data_path),
        sheet_name=scenario_mapper[scenario], index_col=[1], skiprows=3,
        encoding='utf-8')


    df = df.loc[buses]


    carriers = pd.DataFrame(
        Package('https://raw.githubusercontent.com/ZNES-datapackages/technology-cost/master/datapackage.json')
        .get_resource('carrier').read(keyed=True)).set_index(
            ['year', 'carrier', 'parameter']).sort_index()

    techs = {
        'Wind': 'onshore',
        'Wind         North Sea': 'offshore',
        'PV': 'pv',
        'TOTAL GAS': 'ocgt',
        'TOTAL Biomass': 'biomass',
        'RoR (MW)': 'ror',
        'PSP (MW)': 'phs',
        'Hydro with reservoir (MW)': 'rsv',
        'Demand (GWh)': 'load'}

    elements = {}
    for b in df.index:
        for tech_key, tech in techs.items():
            element = {}

            if tech in ['onshore', 'offshore', 'pv']:
                if "onshore" == tech:
                    profile = b + "-onshore-profile"
                    carrier = 'wind'
                    tech = "onshore"
                elif "offshore" == tech:
                    profile = b + "-offshore-profile"
                    carrier = 'wind'
                    tech = "offshore"
                elif "pv" == tech:
                    profile = b + "-pv-profile"
                    carrier = 'solar'
                elif "ror" == tech:
                    profile = b + "-ror-profile"
                    carrier = 'hydro'


                elements['-'.join([b, carrier, tech])] = element

                element.update({
                    "bus": b + "-electricity",
                    "tech": tech,
                    "carrier": carrier,
                    "capacity": round(df.at[b, tech_key], 4),
                    "type": "volatile",
                    "output_parameters": json.dumps({}),
                    "profile": profile,
                    }
                )


            elif tech in ['ocgt', 'st']:
                if tech == 'ocgt':
                    carrier = 'gas'
                else:
                    carrier = 'coal'
                elements['-'.join([b, carrier, tech])] = element

                marginal_cost = float(
                    carriers.at[(scenario_year, carrier, 'cost'), 'value']
                    + carriers.at[(2014, carrier, 'emission-factor'), 'value']
                    * carriers.at[(scenario_year, 'co2', 'cost'), 'value']
                ) / efficiencies[carrier]

                element.update({
                    "carrier": carrier,
                    "capacity": df.at[b, tech_key],
                    "bus": b + "-electricity",
                    "type": "dispatchable",
                    "marginal_cost": marginal_cost,
                    "output_parameters": json.dumps(
                        {"max": avf[carrier]}
                    ),
                    "tech": tech,
                }
            )


            # elif tech == 'phs':
            #     elements['-'.join([b, carrier, tech])] = element
            #
            #     element.update({
            #         'type': 'storage',
            #         'tech': tech,
            #         'bus': b + '-electricity',
            #         'marginal_cost': 0,
            #         'efficiency': efficiencies[tech],
            #         'loss': 0,
            #         'power': df.at[b, tech_key],
            #         'capacity': df.at[b, 'PSP reservoir (GWh)'] * 1000
            #         }
            #     )
            #
            # elif tech == 'rsv':
            #     elements['-'.join([b, carrier, tech])] = element
            #
            #     element.update({
            #         'type': 'reservoir',
            #         'tech': tech,
            #         'inflow': b + 'electricity-rsv-inflow',
            #         'bus': b + '-electricity',
            #         'marginal_cost': 0,
            #         'efficiency': efficiencies[tech],
            #         'capacity': df.at[b, tech_key]
            #     }
            # )

            elif tech == "biomass":
                carrier = "biomass"#
                elements["-".join([b, carrier, 'ce'])] = element

                element.update({
                    "carrier": carrier,
                    "capacity": df.at[b, tech_key],
                    "to_bus": b + "-electricity",
                    "efficiency": efficiencies[carrier],
                    "from_bus": b + "-biomass-bus",
                    "type": "conversion",
                    "carrier_cost": float(
                        carriers.at[(2050, carrier, 'cost'), 'value']
                    ),
                    "tech": 'ce',
                    "output_parameters": json.dumps({})
                    })



    df = pd.DataFrame.from_dict(elements, orient="index")
    df = df.fillna(0)

    df = df[df.capacity != 0]


    for element_type in ['dispatchable', 'volatile', 'conversion', 'storage',
                        'reservoir', 'load']:
        building.write_elements(
            element_type + ".csv",
            df.loc[df["type"] == element_type].dropna(how="all", axis=1),
            directory=os.path.join(datapackage_dir, "data", "elements"),
        )

def excess(datapackage_dir):
    """
    """
    path = os.path.join(datapackage_dir, "data", "elements")
    buses = building.read_elements("bus.csv", directory=path)

    buses.index.name = "bus"
    buses = buses.loc[buses['carrier'] == 'electricity']

    elements = pd.DataFrame(buses.index)
    elements["type"] = "excess"
    elements["carrier"] = "electricity"
    elements["tech"] = "excess"
    elements["name"] = elements["bus"] + "-excess"
    elements["marginal_cost"] = 0

    elements.set_index("name", inplace=True)

    building.write_elements("excess.csv", elements, directory=path)

def shortage(datapackage_dir):
    """
    """
    path = os.path.join(datapackage_dir, "data", "elements")
    buses = building.read_elements("bus.csv", directory=path)

    buses = buses.loc[buses['carrier'] == 'electricity']
    buses.index.name = "bus"

    elements = pd.DataFrame(buses.index)
    elements["capacity"] = 10e10
    elements["type"] = "shortage"
    elements["carrier"] = "electricity"
    elements["tech"] = "shortage"
    elements["name"] = elements["bus"] + "-shortage"
    elements["marginal_cost"] = 300

    elements.set_index("name", inplace=True)

    building.write_elements("shortage.csv", elements, directory=path)
