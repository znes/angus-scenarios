import os
import toml

flex = [0] #range(0, 110, 10)

for dir in os.listdir("scenarios"):
    if not os.path.exists("sensitivities"):
        os.makedirs("sensitivities")
    scenario = toml.load(os.path.join("scenarios", dir))
    for f in flex:
        filename = dir.split(".")[0] + "-flex" + str(f) + ".toml"
        scenario["scenario"]["decentral_flex_share"] = f  / 100
        scenario["name"] = filename.replace(".toml", "")
        scenario["title"] = filename.replace(".toml", "")
        toml_string = toml.dumps(scenario)
        with open(os.path.join("scenarios", filename), mode='w') as w:
            w.writelines(toml_string)
