import os
import toml

flex = [0]

heat = {"2050REF.toml": [-40, -30, -20, -10, 10, 20, 30, 40,]}

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

    if dir in heat.keys():
        for k,v in heat.items():
            for vv in v:
                filename = dir.split(".")[0] + "-load-" + str(vv) + ".toml"
                scenario["sensitivities"].update({"heat": {"DE-decentral_heat-load": 284 * (1 + vv/100)}})
                scenario["name"] = filename.replace(".toml", "")
                scenario["title"] = filename.replace(".toml", "")
                toml_string = toml.dumps(scenario)
                with open(os.path.join("scenarios", filename), mode='w') as w:
                    w.writelines(toml_string)
