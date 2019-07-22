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



def tyndp_generation(buses, vision, scenario, datapackage_dir, raw_data_path):
    """Extracts TYNDP2016 generation data and writes to datapackage for oemof
    tabular usage

    Parameters
    -----------
    buses: list
        List with buses to extract (Names in country codes)
    vision: str
        TYNDP Vision (one of vision1, vision2, vision3, vision4)
    scenario: str
        Name of scenario to be used for cost assumptions etc
    datapackage_dir: string
        Directory for tabular resource
    raw_data_path: string
        Path where raw data file `e-Highway_database_per_country-08022016.xlsx`
        is located
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

    technologies = pd.DataFrame(
        #Package('/home/planet/data/datapackages/technology-cost/datapackage.json')
        Package('https://raw.githubusercontent.com/ZNES-datapackages/angus-input-data/master/technology/datapackage.json')
        .get_resource('technology').read(keyed=True)).set_index(
            ['year', 'parameter', 'carrier', 'tech' ])

    carrier_package = Package(
        'https://raw.githubusercontent.com/ZNES-datapackages/angus-input-data/master/carrier/datapackage.json')

    carrier_cost = pd.DataFrame(
        carrier_package.get_resource('carrier-cost').read(keyed=True)).set_index(
        ['scenario', 'carrier']).sort_index()

    emission_factors = pd.DataFrame(
        carrier_package.get_resource('emission-factor').read(keyed=True)).set_index(
        ['carrier']).sort_index()

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
                elif carrier == 'oil':
                    tech= 'ocgt'
                else:
                    tech = 'st'

                elements['-'.join([b, carrier, tech])] = element
                marginal_cost = float(
                    carrier_cost.at[(scenario, carrier), 'value']
                    + emission_factors.at[carrier, 'value']
                    * carrier_cost.at[(scenario, 'co2'), 'value']
                ) / float(technologies.loc[(2030, "efficiency", carrier, tech), "value"])    \
                + float(technologies.loc[(2030, "vom", carrier, tech), "value"])

                element.update({
                    "carrier": carrier,
                    "capacity": x.at[b, carrier],
                    "bus": b + "-electricity",
                    "type": "dispatchable",
                    "marginal_cost": marginal_cost,
                    "profile": technologies.loc[(2030, "avf", carrier, tech), "value"],
                    "tech": tech,
                    "output_parameters": json.dumps({})
                }
            )

            elif carrier == 'others-non-res':
                carrier = "mixed"
                elements[b + "-" + carrier] = element

                element.update({
                    "carrier": carrier,
                    "capacity": x.at[b, 'others-non-res'],
                    "bus": b + "-electricity",
                    "type": "dispatchable",
                    "output_parameters": json.dumps({}),
                    "marginal_cost": 0,
                    "tech": 'gt',
                    "profile": technologies.loc[(2030, "avf", carrier, 'gt'), "value"]
                }
            )

            elif carrier == "biomass":
                elements["-".join([b, carrier, 'ce'])] = element

                element.update({
                    "carrier": carrier,
                    "capacity": x.at[b, carrier],
                    "to_bus": b + "-electricity",
                    "efficiency": technologies.loc[
                        (2030, "efficiency", carrier, "ce"), "value"],
                    "from_bus": b + "-biomass-bus",
                    "type": "conversion",
                    "carrier_cost": float(
                        carrier_cost.at[(scenario, carrier), 'value']
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




def DE_nep_conventional(datapackage_dir, nep_scenario, bins=0,
                        cost_scenario=None, raw_data_path=None):
    """Extracts NEP2019 generation data and writes to datapackage for oemof
    tabular usage. Uses OPSD powerplant register for efficiency calculation

    Parameters
    -----------
    nep_scenario: str
        Name of nep scenario e.g. C2030, B2030, A2030
    bins: integer
        Number of bins to create from the powerplant register (Default:0)
    cost_scenario: str
        Name of cost scenario from TYNDP2016
    datapackage_dir: string
        Directory for tabular resource
    raw_data_path: string
        Path where raw data file `e-Highway_database_per_country-08022016.xlsx`
        is located
    """

    technologies = pd.DataFrame(
        #Package('/home/planet/data/datapackages/technology-cost/datapackage.json')
        Package('https://raw.githubusercontent.com/ZNES-datapackages/angus-input-data/master/technology/datapackage.json')
        .get_resource('technology').read(keyed=True)).set_index(
            ['year', 'parameter', 'carrier', 'tech' ])

    carrier_package = Package(
        'https://raw.githubusercontent.com/ZNES-datapackages/angus-input-data/master/carrier/datapackage.json')

    carrier_cost = pd.DataFrame(
        carrier_package.get_resource('carrier-cost').read(keyed=True)).set_index(
        ['scenario', 'carrier']).sort_index()

    emission_factors = pd.DataFrame(
        carrier_package.get_resource('emission-factor').read(keyed=True)).set_index(
        ['carrier']).sort_index()

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

    pp = nep.loc[
            (nep["Nettonennleistung " + nep_scenario + " [MW]"] != 0) &
            (nep["Kraftwerkskategorie gemäß Annahme ÜNB (Szenario " + nep_scenario.strip('2030') +")"] !=
                "Kraft-Wärme-Kopplung (KWK)")]["BNetzA-ID"]

    chp = nep.loc[
            (nep["Nettonennleistung " + nep_scenario + " [MW]"] != 0) &
            (nep["Kraftwerkskategorie gemäß Annahme ÜNB (Szenario " + nep_scenario.strip('2030') +")"] ==
                "Kraft-Wärme-Kopplung (KWK)")]["BNetzA-ID"]

    chp_df = nep.loc[chp.index]
    chp_df = chp_df.groupby('Energieträger').sum(axis=1)

    carrier_mapper = {
        "Braunkohle": "lignite",
        "Steinkohle": "coal",
        "Erdgas": "gas",
        "Mineralölprodukte": "oil",
        "Abfall": "waste",
        "Sonstige": "mixed"
    }
    chp_elements = {}

    volatile_profiles = building.read_sequences('volatile_profile.csv',
        directory=os.path.join(datapackage_dir, "data", "sequences"))

    for carrier, row in chp_df.iterrows():
        name = "-".join(["DE", carrier_mapper[carrier], "chp"])
        element = {
            'bus': 'DE-electricity',
            'tech': "chp",
            'carrier': carrier_mapper[carrier],
            'capacity': row["Nettonennleistung " + nep_scenario + " [MW]"],
            'profile': name + "-profile",
            'type': 'volatile'}

        chp_elements[name] = element

        volatile_profiles[name + "-profile"] = pd.read_csv(
            os.path.join(raw_data_path, 'synthetic-heat-load-profile.csv'))['DE']

    volatile_profiles.index = building.timeindex(
        year=str(2030)
    )

    building.write_elements(
        'volatile.csv',
        pd.DataFrame.from_dict(chp_elements, orient='index'),
        directory=os.path.join(datapackage_dir, 'data', 'elements'))

    building.write_sequences(
        'volatile_profile.csv',
        volatile_profiles,
        directory=os.path.join(datapackage_dir, "data", "sequences"))

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
              ('Oil', 'Gas turbine'): ('oil', 'ocgt'),
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

    co2 = carrier_cost.at[(cost_scenario, 'co2'), 'value']

    elements = {}
    for (country, carrier, tech, bins), (capacity, eta) in s.iterrows():
        name = "-".join([country, carrier, tech, str(bins)])

        vom = technologies.at[(2030, 'vom', carrier, tech), 'value']
        ef = emission_factors.at[carrier, 'value']
        fuel = carrier_cost.at[(cost_scenario, carrier), 'value']

        marginal_cost = (fuel + vom + co2 * ef) / Decimal(eta)

        element = {
            'bus': country + '-electricity',
            'tech': tech,
            'carrier': carrier,
            'capacity': capacity,
            'marginal_cost': float(marginal_cost),
            "profile": technologies.loc[(2030, "avf", carrier, tech), "value"],
            'output_parameters': json.dumps({}),
            'type': 'dispatchable'}

        elements[name] = element


    building.write_elements(
        'dispatchable.csv',
        pd.DataFrame.from_dict(elements, orient='index'),
        directory=os.path.join(datapackage_dir, 'data', 'elements'))

def DE_nep(datapackage_dir, raw_data_path, nep_scenario, cost_scenario):
    """Extracts NEP2019 non-conventional generation and storage data

    Parameters
    -----------
    nep_scenario: str
        Name of nep scenario e.g. C2030, B2030, A2030
    cost_scenario: str
        Name of cost scenario from TYNDP2016
    datapackage_dir: string
        Directory for tabular resource
    raw_data_path: string
        Path where raw data file `e-Highway_database_per_country-08022016.xlsx`
        is located
    """
    technologies = pd.DataFrame(
        #Package('/home/planet/data/datapackages/technology-cost/datapackage.json')
        Package('https://raw.githubusercontent.com/ZNES-datapackages/angus-input-data/master/technology/datapackage.json')
        .get_resource('technology').read(keyed=True)).set_index(
            ['year', 'parameter', 'carrier', 'tech' ])

    data = pd.DataFrame(
        Package('https://raw.githubusercontent.com/ZNES-datapackages/angus-input-data/master/capacities/datapackage.json').
        get_resource('DE_system').read(keyed=True)).set_index(["scenario"])

    carrier_package = Package(
        'https://raw.githubusercontent.com/ZNES-datapackages/angus-input-data/master/carrier/datapackage.json')

    carrier_cost = pd.DataFrame(
        carrier_package.get_resource('carrier-cost').read(keyed=True)).set_index(
        ['scenario', 'carrier']).sort_index()

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
                "efficiency": technologies.loc[(2030, 'efficiency', 'biomass', 'st'), 'value'],
                "maringal_cost": technologies.loc[(2030, 'vom', 'biomass', 'st'), 'value'],
                "from_bus": b + "-biomass-bus",
                "type": "conversion",
                "carrier_cost": float(
                    carrier_cost.at[(cost_scenario, carrier), 'value']
                ),
                "tech": 'ce',
                }
            )

    elements['DE-battery'] =    {
            "storage_capacity": technologies.loc[
                (2030, 'efficiency', 'lithium', 'battery'), 'value'] * \
                data.loc[nep_scenario, "battery"],
            "capacity": data.loc[nep_scenario, "battery"],
            "bus": "DE-electricity",
            "tech": 'battery',
            "carrier": 'lithium',
            "type": "storage",
            "efficiency": float(technologies.loc[(2030, 'efficiency', 'lithium', 'battery'), 'value'])**0.5,  # convert roundtrip to input / output efficiency
            "marginal_cost": 0,
            "loss": 0
        }

    # update DE load in the load.csv resource
    load = building.read_elements(
        "load.csv",
        directory=os.path.join(datapackage_dir, "data", "elements"))

    load.loc['DE-electricity-load', 'amount'] = data.loc[nep_scenario, "demand"] * 1000

    building.write_elements(
        "load.csv", load,
        directory=os.path.join(datapackage_dir, "data", "elements"),
        replace=True
    )

    df = pd.DataFrame.from_dict(elements, orient="index")


    for element_type in ['volatile', 'conversion', 'storage']:
        building.write_elements(
            element_type + ".csv",
            df.loc[df["type"] == element_type].dropna(how="all", axis=1),
            directory=os.path.join(datapackage_dir, "data", "elements")
        )

def ehighway_generation(
    buses, cost_scenario, scenario="100% RES", datapackage_dir=None,
    raw_data_path=None):
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

    technologies = pd.DataFrame(
        #Package('/home/planet/data/datapackages/technology-cost/datapackage.json')
        Package('https://raw.githubusercontent.com/ZNES-datapackages/angus-input-data/master/technology/datapackage.json')
        .get_resource('technology').read(keyed=True)).set_index(
            ['year', 'parameter', 'carrier', 'tech' ])


    carrier_package = Package(
        'https://raw.githubusercontent.com/ZNES-datapackages/angus-input-data/master/carrier/datapackage.json')

    carrier_cost = pd.DataFrame(
        carrier_package.get_resource('carrier-cost').read(keyed=True)).set_index(
        ['scenario', 'carrier']).sort_index()

    emission_factors = pd.DataFrame(
        carrier_package.get_resource('emission-factor').read(keyed=True)).set_index(
        ['carrier']).sort_index()

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
                    carrier_cost.at[(cost_scenario, carrier), 'value']
                    + emission_factors.at[carrier, 'value']
                    * carrier_cost.at[(cost_scenario, 'co2'), 'value']
                    / technologies.loc[(2050, 'efficiency', carrier, tech), "value"] +
                    technologies.loc[(2050, 'vom', carrier, tech), "value"]
                    )

                element.update({
                    "carrier": carrier,
                    "capacity": df.at[b, tech_key],
                    "bus": b + "-electricity",
                    "type": "dispatchable",
                    "marginal_cost": marginal_cost,
                    "profile": technologies.loc[(2050, 'avf', carrier, tech), "value"],
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
                # tech is actually 'ce', kind of hackisch works for now
                carrier = "biomass"#
                elements["-".join([b, carrier, 'ce'])] = element

                element.update({
                    "carrier": carrier,
                    "capacity": df.at[b, tech_key],
                    "to_bus": b + "-electricity",
                    "efficiency": technologies.loc[(2050, 'efficiency', carrier, 'ce'), "value"],
                    "marginal_cost": technologies.loc[(2050, 'vom', carrier, 'ce'), "value"],
                    "from_bus": b + "-biomass-bus",
                    "type": "conversion",
                    "carrier_cost": float(
                        carrier_cost.at[(cost_scenario, carrier), 'value']
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
    elements["marginal_cost"] = 3000

    elements.set_index("name", inplace=True)

    building.write_elements("shortage.csv", elements, directory=path)
