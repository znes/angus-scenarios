import os
import toml

demand = {
    "2030DG.toml": "2030GS" ,
    "2040DG.toml": "2040GS",
    "2050REF.toml": "2050GS"}

for k,v  in demand.items():
    scenario = toml.load(os.path.join("scenarios", k))
    filename = k.split(".")[0] + "-GS.toml"
    scenario["scenario"]["DE_heat_system"] = v
    scenario["scenario"]["decentral_heat-flex-share"] = 1
    scenario["name"] = filename.replace(".toml", "")
    scenario["title"] = filename.replace(".toml", "")
    toml_string = toml.dumps(scenario)
    with open(os.path.join("scenarios", filename), mode='w') as w:
        w.writelines(toml_string)

biomass_share = [0, 20, 40, 60, 80]
for dir in os.listdir("scenarios"):
    scenario = toml.load(os.path.join("scenarios", dir))
    for b in biomass_share:
        if "2050REF.toml" in dir:
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
