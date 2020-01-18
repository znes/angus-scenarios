# -*- coding: utf-8 -*-
"""
"""
import os
from datapackage import Package
import json
import pandas as pd

from oemof.tabular.datapackage import building


def _get_hydro_inflow(inflow_dir=None):
    """ Adapted from:

            https://github.com/FRESNA/vresutils/blob/master/vresutils/hydro.py
    """

    def read_inflow(country):
        return pd.read_csv(
            os.path.join(inflow_dir, "Hydro_Inflow_{}.csv".format(country)),
            parse_dates={"date": [0, 1, 2]},
        ).set_index("date")["Inflow [GWh]"]

    europe = [
        "AT",
        "BA",
        "BE",
        "BG",
        "CH",
        "CZ",
        "DE",
        "ES",
        "FI",
        "FR",
        "HR",
        "HU",
        "IE",
        "IT",
        "KV",
        "LT",
        "LV",
        "ME",
        "MK",
        "NL",
        "NO",
        "PL",
        "PT",
        "RO",
        "RS",
        "SE",
        "SI",
        "SK",
        "UK",
    ]

    hyd = pd.DataFrame({cname: read_inflow(cname) for cname in europe})

    hyd.rename(columns={"UK": "GB"}, inplace=True)  # for ISO country code

    hydro = hyd.resample("H").interpolate("cubic")

    # add last day of the dataset that is missing from resampling
    last_day = pd.DataFrame(
        index=pd.DatetimeIndex(start="20121231", freq="H", periods=24),
        columns=hydro.columns,
    )
    data = hyd.loc["2012-12-31"]
    for c in last_day:
        last_day.loc[:, c] = data[c]

    # need to drop last day because it comes in last day...
    hydro = pd.concat([hydro.drop(hydro.tail(1).index), last_day])

    # remove last day in Feb for leap years
    hydro = hydro[~((hydro.index.month == 2) & (hydro.index.day == 29))]

    if True:  # default norm
        normalization_factor = hydro.index.size / float(
            hyd.index.size
        )  # normalize to new sampling frequency
    # else:
    #     # conserve total inflow for each country separately
    #    normalization_factor = hydro.sum() / hyd.sum()
    hydro /= normalization_factor

    return hydro


def generation(config, scenario_year, datapackage_dir, raw_data_path):
    """
    """
    countries, scenario_year = (
        config["buses"]["electricity"],
        config["scenario"]["year"],
    )

    building.download_data(
        "https://zenodo.org/record/804244/files/Hydro_Inflow.zip?download=1",
        directory=raw_data_path,
        unzip_file="Hydro_Inflow/",
    )

    technologies = pd.DataFrame(
        Package(
            "https://raw.githubusercontent.com/ZNES-datapackages/"
            "angus-input-data/master/technology/datapackage.json"
        )
        .get_resource("technology")
        .read(keyed=True)
    ).set_index(["year", "parameter", "carrier", "tech"])

    hydro_data = pd.DataFrame(
        Package(
            "https://raw.githubusercontent.com/ZNES-datapackages/"
            "angus-input-data/master/hydro/datapackage.json"
        )
        .get_resource("hydro")
        .read(keyed=True)
    ).set_index(["year","country"])

    hydro_data.rename(index={"UK": "GB"}, inplace=True)  # for iso code

    inflows = _get_hydro_inflow(
        inflow_dir=os.path.join(raw_data_path, "Hydro_Inflow")
    )

    inflows = inflows.loc[
        inflows.index.year == config["scenario"]["weather_year"], :
    ]

    inflows["DK"], inflows["LU"] = 0, inflows["BE"]

    for c in hydro_data.columns:
        if c != "source":
            hydro_data[c] = hydro_data[c].astype(float)

    capacities =  hydro_data.loc[scenario_year].loc[countries][["ror", "rsv", "phs"]]
    ror_shares =  hydro_data.loc[scenario_year].loc[countries]["ror-share"]
    max_hours =  hydro_data.loc[scenario_year].loc[countries][["rsv-max-hours", "phs-max-hours"]]


    # ror
    elements = {}
    for country in countries:
        name = country + "-hydro-ror"

        capacity = capacities.loc[country, "ror"]

        eta = technologies.loc[
            (scenario_year, "efficiency", "hydro", "ror"), "value"
        ]

        if capacity > 0:

            elements[name] = {
                "type": "volatile",
                "tech": "ror",
                "carrier": "hydro",
                "bus": country + "-electricity",
                "capacity": capacity,
                "profile": country + "-ror-profile",
                "efficiency": eta,
            }

    building.write_elements(
        "ror.csv",
        pd.DataFrame.from_dict(elements, orient="index"),
        directory=os.path.join(datapackage_dir, "data", "elements"),
    )

    sequences = (inflows[countries] * ror_shares * 1000) / capacities["ror"]
    sequences = sequences[countries].copy()
    sequences.dropna(axis=1, inplace=True)
    sequences.clip(upper=1, inplace=True)
    sequences.columns = sequences.columns.astype(str) + "-ror-profile"

    building.write_sequences(
        "ror_profile.csv",
        sequences.set_index(building.timeindex(str(scenario_year))),
        directory=os.path.join(datapackage_dir, "data", "sequences"),
    )

    # reservoir
    elements = {}
    for country in countries:
        name = country + "-hydro-reservoir"

        capacity = capacities.loc[country, "rsv"]
        rsv_max_hours = max_hours.loc[country, "rsv-max-hours"]

        eta = technologies.loc[
            (scenario_year, "efficiency", "hydro", "rsv"), "value"
        ]

        if capacity > 0:
            elements[name] = {
                "type": "reservoir",
                "tech": "rsv",
                "carrier": "hydro",
                "bus": country + "-electricity",
                "capacity": capacity,
                "storage_capacity": capacity * rsv_max_hours,
                "profile": country + "-reservoir-profile",
                "efficiency": eta,
                "marginal_cost": 0.0000001,
            }

    building.write_elements(
        "reservoir.csv",
        pd.DataFrame.from_dict(elements, orient="index"),
        directory=os.path.join(datapackage_dir, "data", "elements"),
    )

    sequences = inflows[countries] * (1 - ror_shares) * 1000 * 1.7 # correction factor for eHighway inflow
    sequences = sequences[countries].copy()
    sequences.dropna(axis=1, inplace=True)
    sequences.columns = sequences.columns.astype(str) + "-reservoir-profile"
    building.write_sequences(
        "reservoir_profile.csv",
        sequences.set_index(building.timeindex(str(scenario_year))),
        directory=os.path.join(datapackage_dir, "data", "sequences"),
    )

    # phs
    elements = {}
    for country in countries:
        name = country + "-hydro-phs"

        capacity = capacities.loc[country, "phs"]
        phs_max_hours = max_hours.loc[country, "phs-max-hours"]

        eta = technologies.loc[
            (scenario_year, "efficiency", "hydro", "phs"), "value"
        ]

        if capacity > 0:

            elements[name] = {
                "type": "storage",
                "tech": "phs",
                "carrier": "hydro",
                "bus": country + "-electricity",
                "capacity": capacity,
                "loss": 0,
                "marginal_cost": 1,
                "storage_capacity": capacity * phs_max_hours,
                "storage_capacity_initial": 0.5,
                "efficiency": float(eta)
                ** (0.5),  # rountrip to input/output eta
            }

    building.write_elements(
        "phs.csv",
        pd.DataFrame.from_dict(elements, orient="index"),
        directory=os.path.join(datapackage_dir, "data", "elements"),
    )
