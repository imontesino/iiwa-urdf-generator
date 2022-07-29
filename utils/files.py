from pathlib import Path
from typing import List
from unicodedata import name


def get_component_file(name):
    found = False
    for path in Path('src/urdf/components').rglob('*.sdf.j2'):
        if path.name.split('.')[0] == name:
            found = True
            break

    if found:
        return str(path).replace('src/', '')
    else:
        raise FileNotFoundError(f"Component {name} has no file assosicated with it")


def get_component(name):
    component_file = get_component_file(name)

    with open(component_file, "r", encoding="utf-8") as f:
        data = f.read()
        print(data)

    return data

def choose_file(base_path, ending, recursive=False, filetype_name="file"):
    files: List[Path] = []

    if recursive:
        for path in Path(base_path).rglob('*'+ending):
            files.append(path)
    else:
        for path in Path(base_path).glob('*'+ending):
            files.append(path)

    if len(files) == 0:
        print(f"No '{ending}' files found, try recursive=True")
        return None

    for i, config_file in enumerate(files):
        print(f"{i}: {config_file.name}")

    while True:
        choice = input(f"Choose a {filetype_name}: ")
        if choice.isdigit() and int(choice) in range(len(files)):
            choice = int(choice)
            break
        else:
            print("Invalid choice")

    return files[choice]