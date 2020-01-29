import json
import logging
import os
import pandas as pd

import multiprocessing as mp

from oemof.solph import Bus, EnergySystem, Model, constraints
from oemof.tabular import facades
from oemof.tabular.datapackage import aggregation, processing
from oemof.tabular.tools import postprocessing as pp
import oemof.outputlib as outputlib

from pyomo.environ import Expression

from fuchur.cli import Scenario



def compute(
    datapackage, solver="gurobi"
):
    """
    """
    config = Scenario.from_path(
        os.path.join("scenarios", datapackage + ".toml"))
    emission_limit = config["scenario"].get("co2_limit")

    temporal_resolution = config.get("model", {}).get("temporal_resolution", 1)

    datapackage_dir = os.path.join("datapackages", datapackage)

    # create results path
    scenario_path = os.path.join("results", datapackage)
    if not os.path.exists(scenario_path):
        os.makedirs(scenario_path)
    output_path = os.path.join(scenario_path, "output")

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # copy package either aggregated or the original one (only data!)
    if temporal_resolution > 1:
        logging.info("Aggregating for temporal aggregation ... ")
        path = aggregation.temporal_skip(
            os.path.join(datapackage_dir, "datapackage.json"),
            temporal_resolution,
            path=scenario_path,
            name="input",
        )
    else:
        path = processing.copy_datapackage(
            os.path.join(datapackage_dir, "datapackage.json"),
            os.path.abspath(os.path.join(scenario_path, "input")),
            subset="data",
        )

    es = EnergySystem.from_datapackage(
        os.path.join(path, "datapackage.json"),
        attributemap={},
        typemap=facades.TYPEMAP,
    )

    m = Model(es)

    if emission_limit is not None:
        constraints.emission_limit(m, limit=emission_limit)

    flows = {}
    for (i, o) in m.flows:
        if hasattr(m.flows[i, o], "emission_factor"):
            flows[(i, o)] = m.flows[i, o]

    # add emission as expression to model
    BUSES = [b for b in es.nodes if isinstance(b, Bus)]
    def emission_rule(m, b, t):
        expr = sum(m.flow[inflow, outflow, t]
               * m.timeincrement[t]
               * getattr(flows[inflow, outflow], "emission_factor", 0)
               for (inflow, outflow) in flows if outflow is b
              )
        return expr
    m.emissions = Expression(BUSES, m.TIMESTEPS, rule=emission_rule)

    m.receive_duals()

    m.solve(solver)

    m.results = m.results()


    pp.write_results(m, output_path)

    modelstats = outputlib.processing.meta_results(m)
    modelstats.pop("solver")
    modelstats["problem"].pop("Sense")
    # TODO: This is not model stats -> move somewhere else!
    modelstats["temporal_resolution"] = temporal_resolution
    modelstats["emission_limit"] = emission_limit

    with open(os.path.join(scenario_path, "modelstats.json"), "w") as outfile:
        json.dump(modelstats, outfile, indent=4)

    supply_sum = (
        pp.supply_results(
            results=m.results,
            es=m.es,
            bus=[b.label for b in es.nodes if isinstance(b, Bus)],
            types=[
                "dispatchable",
                "volatile",
                "conversion",
                "backpressure",
                "extraction",
            #    "storage",
                "reservoir",
            ],
        )
        #.clip(0)
        .sum()
        .reset_index()
    )
    supply_sum["from"] = supply_sum.apply(
        lambda x: "-".join(x["from"].label.split("-")[1::]), axis=1
    )
    supply_sum.drop("type", axis=1, inplace=True)
    supply_sum = (
        supply_sum.set_index(["from", "to"]).unstack("from")
        / 1e6
        * temporal_resolution
    )
    supply_sum.columns = supply_sum.columns.droplevel(0)
    summary = supply_sum  # pd.concat([supply_sum, excess_share], axis=1)
    ## grid
    imports = pd.DataFrame()
    link_results = pp.component_results(m.es, m.results).get("link")
    for b in [b.label for b in es.nodes if isinstance(b, Bus)]:
        if link_results is not None and m.es.groups[b] in list(
            link_results.columns.levels[0]
        ):
            ex = link_results.loc[
                :, (m.es.groups[b], slice(None), "flow")
            ].sum(axis=1)
            im = link_results.loc[
                :, (slice(None), m.es.groups[b], "flow")
            ].sum(axis=1)

            net_import = im - ex
            net_import.name = m.es.groups[b]
            imports = pd.concat([imports, net_import], axis=1)

    summary["total_supply"] = summary.sum(axis=1)
    summary["RE-supply"] = (
        summary["wind-onshore"] +
        summary["wind-offshore"] +
        summary["biomass-st"] +
        summary["hydro-ror"] +
        summary["hydro-reservoir"] +
        summary["solar-pv"])
    if "other-res" in summary:
        summary["RE-supply"] += summary["other-res"]

    summary["RE-share"] = summary["RE-supply"] / summary["total_supply"]

    summary["import"] = imports[imports > 0].sum() / 1e6 * temporal_resolution
    summary["export"] = imports[imports < 0].sum() / 1e6 * temporal_resolution
    summary.to_csv(os.path.join(scenario_path, "summary.csv"))

    emissions = pd.Series(
        {key: value() for key,value in m.emissions.items()}).unstack().T
    emissions.to_csv(os.path.join(scenario_path, "emissions.csv"))



if __name__ == "__main__":
    # scenarios = ["2050ANGUS-invest-2040grid"]
    # for s in scenarios:
    #      compute(s, "gurobi")

    datapackages = [d for d in os.listdir("datapackages")]
    p = mp.Pool(1)
    p.map(compute, datapackages)
