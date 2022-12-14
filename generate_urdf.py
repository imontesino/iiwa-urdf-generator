#!/usr/bin/env python3
from email.policy import default
from pyexpat import model
from jinja2 import Environment, FileSystemLoader
import yaml
from utils.files import choose_file
from utils.types import load_components

"""
Compile templates into URDF robot description
"""

template_dir = 'src'
mesh_folder = "src/urdf/meshes"

urdf_template = choose_file(template_dir, '.urdf.j2', filetype_name='URDF template')

config_yaml_path = choose_file('configs', '.yaml', filetype_name='config file')

components = load_components(config_yaml_path, mesh_folder=mesh_folder)

default_name = urdf_template.name.split(".")[0] + '_' + config_yaml_path.name.split(".")[0]

while True:
    name = input(f"Choose name for the urdf model (default: {default_name}): ")
    if name == "":
        name = default_name
        break
    if name.isalnum():
        break
    else:
        print("Invalid name")

# Generate template
loader = FileSystemLoader(searchpath="./src/")
env = Environment(loader=loader, autoescape=True)
env.trim_blocks = True
env.lstrip_blocks = True

if __name__ == "__main__":
    # Load and compile Jinja2 templates when executed
    template = env.get_template(urdf_template.name)
    with open(name+".urdf", "w") as f:
        f.write(template.render(name=name,
                                links=components["links"],
                                joints=components["joints"],
                                materials=components["materials"]))
