# -*- coding: utf-8 -*-
"""
"""
import os
from datetime import datetime

from oemof.tabular.datapackage import building
import pandas as pd


def ninja_pv_profiles(buses, weather_year, scenario_year, datapackage_dir,
       raw_data_path):
    """
    Parameter
    ---------
    buses: array like
        List with buses represented by iso country code
    weather_year: integer or string
        Year to select from raw data source
    scenario_year: integer or string
        Year to use for timeindex in tabular resource
    datapackage_dir: string
        Directory for tabular resource
    raw_data_path: string
        Path where raw data file `ninja_pv_europe_v1.1_merra2.csv`
        is located
    """
    filepath = building.download_data(
        "https://www.renewables.ninja/static/downloads/ninja_europe_pv_v1.1.zip",
        unzip_file="ninja_pv_europe_v1.1_merra2.csv",
        directory=raw_data_path)

    year = str(weather_year)

    countries = buses

    raw_data = pd.read_csv(filepath, index_col=[0], parse_dates=True)
    # for leap year...
    raw_data = raw_data[
        ~((raw_data.index.month == 2) & (raw_data.index.day == 29))
    ]

    df = raw_data.loc[year]

    sequences_df = pd.DataFrame(index=df.index)

    for c in countries:
        sequence_name = c + "-pv-profile"
        sequences_df[sequence_name] = raw_data.loc[year][c].values

    sequences_df.index = building.timeindex(
        year=str(scenario_year)
    )
    building.write_sequences(
        "volatile_profile.csv",
        sequences_df,
        directory=os.path.join(datapackage_dir, "data", "sequences"),
    )


def ninja_wind_profiles(buses, weather_year, scenario_year, datapackage_dir,
         raw_data_path):
    """
    Parameter
    ---------
    buses: array like
        List with buses represented by iso country code
    weather_year: integer or string
        Year to select from raw data source
    scenario_year: integer or string
        Year to use for timeindex in tabular resource
    datapackage_dir: string
        Directory for tabular resource
    raw_data_path: string
        Path where raw data file `ninja_wind_europe_v1.1_current_national.csv`
        and `ninja_wind_europe_v1.1_current_national.csv`
        is located
    """
    near_term_path = building.download_data(
        "https://www.renewables.ninja/static/downloads/ninja_europe_wind_v1.1.zip",
        unzip_file= "ninja_wind_europe_v1.1_current_national.csv",
        directory=raw_data_path)

    onoff_filepath = building.download_data(
        "https://www.renewables.ninja/static/downloads/ninja_europe_wind_v1.1.zip",
        unzip_file= "ninja_wind_europe_v1.1_future_nearterm_on-offshore.csv",
        directory=raw_data_path)

    year = str(weather_year)

    near_term = pd.read_csv(near_term_path, index_col=[0], parse_dates=True)
    # for lead year...
    near_term = near_term[
        ~((near_term.index.month == 2) & (near_term.index.day == 29))
    ]

    on_off_data = pd.read_csv(onoff_filepath, index_col=[0], parse_dates=True)
    on_off_data = on_off_data[
        ~((on_off_data.index.month == 2) & (on_off_data.index.day == 29))
    ]

    sequences_df = pd.DataFrame(index=near_term.loc[year].index)

    NorthSea = ["DE", "DK", "NO", "NL", "BE", "GB", "SE"]

    for c in buses:
        # add offshore profile if country exists in offshore data columns
        # and if its in NorthSea
        if [
            c + "_OFF" in on_off_data.columns
        ] and c in NorthSea:
            sequences_df[c + "-offshore-profile"] = on_off_data[c + "_OFF"]

            if c + "_ON" in on_off_data.columns:
                sequence_name = c + "-onshore-profile"
                sequences_df[sequence_name] = on_off_data[c + "_ON"]
            else:
                # for all countries that are not in the on/off data set use current
                # national
                sequence_name = c + "-onshore-profile"
                sequences_df[sequence_name] = near_term.loc[year][c].values
        else:
            # for all countries that are not in the on/off data set use current
            # national
            sequence_name = c + "-onshore-profile"
            sequences_df[sequence_name] = near_term.loc[year][c].values


    sequences_df.index = building.timeindex(
        year=str(scenario_year)
    )

    building.write_sequences(
        "volatile_profile.csv",
        sequences_df,
        directory=os.path.join(datapackage_dir, "data", "sequences"),
    )


def emhires_wind_profiles(
    buses, weather_year, scenario_year, datapackage_dir, raw_data_path):
    """
    Gonzalez Aparicio, Iratxe; Zucker, Andreas; Careri, Francesco;
    Monforti Ferrario, Fabio; Huld, Thomas; Badger, Jake (2016):
    Wind hourly generation time series at country, NUTS 1,
    NUTS 2 level and bidding zones. European Commission, Joint Research Centre (JRC) [Dataset]
    PID: http://data.europa.eu/89h/jrc-emhires-wind-generation-time-series
    """
    year = str(weather_year)
    countries = buses


    date_parser = lambda y: datetime.strptime(y, '%Y %m %d %H')
    date_columns = ['Year', 'Month', 'Day', 'Hour']

    urls =  [
        'http://setis.ec.europa.eu/sites/default/files/EMHIRES_DATA/EMHIRES_WIND_COUNTRY_June2019.zip',
        'http://setis.ec.europa.eu/sites/default/files/EMHIRES_DATA/TS_CF_OFFSHORE_30yr_date.zip'
    ]
    filenames = [
        'EMHIRES_WIND_COUNTRY_June2019.xlsx',
        'TS.CF.OFFSHORE.30yr.date.txt']
    technologies = [
        'onshore',
        'offshore']

    for url, fname, tech in zip(urls, filenames, technologies):
        if fname.endswith('.xlsx'):
            df = pd.read_excel(building.download_data(
                url, unzip_file=fname, directory=raw_data_path),
                parse_dates={'i': date_columns}, date_parser=date_parser,
                index_col='i').reindex(columns=countries).dropna(axis=1).loc[year, :]
        else:
            df = pd.read_csv(building.download_data(
                url, unzip_file=fname, directory=raw_data_path), sep='\t',
                parse_dates={'i': date_columns}, date_parser=date_parser,
                index_col='i').reindex(columns=countries).dropna(axis=1).loc[year, :]
        renames = {c: c + '-' + tech + '-profile' for c in countries}

        df.rename(columns=renames, inplace=True)

        df = df[
            ~((df.index.month == 2) & (df.index.day == 29))
        ]

        df.index = building.timeindex(
            year=str(scenario_year)
        )

        building.write_sequences(
            'volatile_profile.csv', df,
            directory=os.path.join(datapackage_dir, "data", "sequences"))


def emhires_pv_profiles(
    buses, weather_year, scenario_year, datapackage_dir, raw_data_path):

    """
    Gonzalez Aparicio, Iratxe (2017):  Solar hourly generation time series
    at country, NUTS 1, NUTS 2 level and bidding zones. European Commission,
    Joint Research Centre (JRC) [Dataset]
    PID: http://data.europa.eu/89h/jrc-emhires-solar-generation-time-series
    EU Commission, DG ENER, Unit A4 - ENERGY STATISTICS,
    https://ec.europa.eu/energy/sites/ener/files/documents/countrydatasheets_june2018.xlsx

    """
    year = str(weather_year)
    countries = buses

    date_parser = lambda y: datetime.strptime(y, '%Y %m %d %H')
    date_columns = ['Year', 'Month', 'Day', 'Hour']

    df = pd.read_excel(
            building.download_data(
            'https://setis.ec.europa.eu/sites/default/files/EMHIRES_DATA/Solar/EMHIRESPV_country_level.zip',
            unzip_file='EMHIRESPV_TSh_CF_Country_19862015.xlsx',
            directory=raw_data_path),
            parse_dates={'i': date_columns}, date_parser=date_parser,
            index_col='i').reindex(columns=countries).dropna(axis=1).loc[year, countries]

    renames = {c: c + '-pv-profile' for c in countries}

    df.rename(columns=renames, inplace=True)

    df = df[
        ~((df.index.month == 2) & (df.index.day == 29))
    ]

    df.index = building.timeindex(
        year=str(scenario_year)
    )

    building.write_sequences(
        'volatile_profile.csv', df,
        directory=os.path.join(datapackage_dir, "data", "sequences"))


#
# from oemof.tabular.datapackage import building
# import pandas as pd
# import os
# seq = building.download_data(
#     "https://github.com/znes/FlEnS/archive/master.zip",
#     unzip_file= "FlEnS-master/",
#     directory="/home/admin/fuchur-raw-data")
# long = pd.read_csv(
#     os.path.join(seq, "FlEnS-master", "Socio-ecologic", "2050_seq.csv"),
#     header=[0,1,2,3,4,5], parse_dates=True, index_col=0)
# long.columns = long.columns.droplevel([0,2,3,4])




year='2012'
profiles = ninja_wind_profiles
profiles(["DE"], year, 2030, os.path.join("datapackages", "ninja"), "/home/admin/fuchur-raw-data")


# import pandas as pd
# from oemof.tabular.datapackage import building
# heat_path = building.download_data(
#     "https://gitlab.com/hotmaps/load_profile/load_profile_residential_heating_generic/raw/master/data/hotmaps_task_2.7_load_profile_residential_heating_generic.csv",
#     directory="/home/admin/fuchur-raw-data")
# df = pd.read_csv(heat_path)
#
# df = pd.concat(
#     [
#         pd.DataFrame(
#             df["NUTS2_code"].apply(lambda row: [row[0:2], row[2:4]]).tolist(),
#             columns=["nuts", "code"],
#         ),
#         df,
#     ],
#     axis=1,
# )
# df = df.set_index(['nuts', "code"])
# df.loc["DE"].groupby(['temperature', 'hour']).mean()
#
# de = df.loc["DE"]
# len(de['load'].unique())
# de[(de['hour'] == 12) & (de["temperature"] == -11)]
# # p = Package("https://gitlab.com/hotmaps/load_profile/load_profile_residential_heating_generic/raw/master/datapackage.json")
# import pdb;pdb.set_trace()
# #r = p.get_resource('lp_residential_heating_generic').read(keyed=True)
