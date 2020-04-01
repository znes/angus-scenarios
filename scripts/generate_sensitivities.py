import os
import toml

heat = {"2050REF.toml": [-30, -25, -20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30],
        "2050REF-GS.toml": [-30, -25, -20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30]}
total_demand = {"2050REF-GS.toml": 184000, "2050REF.toml": 284000}

for dir in os.listdir("scenarios"):
    scenario = toml.load(os.path.join("scenarios", dir))
    if dir in heat.keys():
        for k,v in heat.items():
            for vv in v:
                filename = dir.split(".")[0] + "-load-" + str(vv) + ".toml"
                scenario["sensitivities"].update({"heat": {"DE-decentral_heat-load": total_demand[k] * (1 + vv/100)}})
                scenario["scenario"]["decentral_heat-flex-share"] = 1
                scenario["name"] = filename.replace(".toml", "")
                scenario["title"] = filename.replace(".toml", "")
                toml_string = toml.dumps(scenario)
                with open(os.path.join("scenarios", filename), mode='w') as w:
                    w.writelines(toml_string)

biomass_share = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
for dir in os.listdir("scenarios"):
    scenario = toml.load(os.path.join("scenarios", dir))
    for b in biomass_share:
        if "2050REF" in dir:
            if not "-load" in dir:
                filename = dir.split(".")[0] + "-bio-" + str(b) + ".toml"
                scenario["sensitivities"].update({"biomass": {"DE-biomass-commodity": b / 100}})
                scenario["scenario"]["decentral_heat-flex-share"] = 1
                scenario["name"] = filename.replace(".toml", "")
                scenario["title"] = filename.replace(".toml", "")
                toml_string = toml.dumps(scenario)
                with open(os.path.join("scenarios", filename), mode='w') as w:
                    w.writelines(toml_string)

flex = [0]
for dir in os.listdir("scenarios"):
    scenario = toml.load(os.path.join("scenarios", dir))
    for f in flex:
        filename = dir.split(".")[0] + "-flex" + str(f) + ".toml"
        scenario["scenario"]["decentral_heat-flex-share"] = f  / 100
        scenario["name"] = filename.replace(".toml", "")
        scenario["title"] = filename.replace(".toml", "")
        toml_string = toml.dumps(scenario)
        with open(os.path.join("scenarios", filename), mode='w') as w:
            w.writelines(toml_string)
