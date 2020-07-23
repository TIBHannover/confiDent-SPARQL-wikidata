import yaml
from pathlib import Path
from typing import Dict


def relative_read_f(relativepath2f: str) -> str:
    path_file = Path(__file__).parent / relativepath2f
    with open(path_file, 'r') as f:
        f_content = f.read()
    return f_content


def yaml2dict(path: str) -> Dict:
    with open(path, 'r') as yaml_f:
        yaml_content = yaml_f.read()
        yaml_dict = yaml.safe_load(yaml_content)
    return yaml_dict


def yaml_get_source(relativepath2f: str) -> Dict:
    path_file = Path(__file__).parent / relativepath2f
    yamldict = yaml2dict(path_file)
    return yamldict


def yaml_get_mapping(mapping: str) -> Dict:
    confid2ext_schema = yaml_get_source(f'../mapping2confident/{mapping}.yml')
    # ext_schema = list(confid2ext_schema.keys())[0]
    # ext_schema_mapping = confid2ext_schema[ext_schema]
    return confid2ext_schema

