import pathlib
import yaml

from .files import get_component_file

COMPONENT_TYPES = ['link', 'joint']

def get_component_type(component_config, name):
    print(name, component_config)
    for component_type in COMPONENT_TYPES:
        if component_type in name:
            return component_type
        if component_config is not None and "type" in component_config:
            if component_config["type"] == component_type:
                return component_type

    err_msg = f"Error found in cnfig for component {name}\n"
    err_msg += "Component type not found in config or not valid (joint, link):\n"
    err_msg += yaml.dump(component_config)

    raise SyntaxError(err_msg)

def load_components(yaml_file: pathlib.Path, mesh_folder="meshes"):
    config = yaml.safe_load(open(yaml_file))

    if "parent" in config:
        parent_file = pathlib.Path(yaml_file.parent, config["parent"]+".yaml")
        components = load_components(parent_file, mesh_folder)
    else:
        components = {
            "links": [],
            "joints": [],
            "materials": []
        }

    if "components" in config:
        for component_definition_key in config["components"]:
            component_config = config["components"][component_definition_key]
            component_type = get_component_type(component_config, component_definition_key)
            component = {
                "name": component_definition_key,
                "file": get_component_file(component_definition_key)
            }
            if component_type == "link":
                component["material"] = component_config["material"]
                component["mesh_folder"] = mesh_folder
                components["links"].append(component)
            elif component_type == "joint":
                components["joints"].append(component)

        for i, joint in enumerate(components["joints"]):
            joint["parent_link_name"] = components["links"][i]["name"]
            joint["child_link_name"] = components["links"][i+1]["name"]

    if "materials" in config:
        for key in config["materials"]:
            components["materials"].append(
                {
                    "name": config["materials"][key]["name"],
                    "color": config["materials"][key]["color"],
                }
            )

    return components

