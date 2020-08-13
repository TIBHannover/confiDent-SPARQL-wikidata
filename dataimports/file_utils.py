import yaml
import sys
from pathlib import Path
from typing import Dict
from dataimports.globals import Colors


def wikidetails_present():
    wikidetails = Path(__file__).parent.parent / 'wikidetails.yml'
    if not wikidetails.is_file():
        print(f'{Colors.FAIL}Error: {wikidetails} file is essential to '
              f'write to the wiki is missing. Use wikidetails.yml.template '
              f'to create it.{Colors.ENDC}')
        sys.exit(1)


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
    # print('CWD:', Path.cwd())
    # print('parent:', Path(__file__).parent)
    path_file = Path(__file__).parent / relativepath2f
    yamldict = yaml2dict(path_file)
    return yamldict


def yaml_get_mapping(mapping: str) -> Dict:
    confid2ext_schema = yaml_get_source(f'../mapping2confident/{mapping}.yml')
    # ext_schema = list(confid2ext_schema.keys())[0]
    # ext_schema_mapping = confid2ext_schema[ext_schema]
    return confid2ext_schema
