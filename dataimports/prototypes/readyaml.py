import sys
from pathlib import Path

cwd = Path.cwd()
sys.path.append(f'{cwd}/dataimports')
from file_utils import yaml_get_source

subobject_mapping = yaml_get_source('prototypes/mapping_subobject.yml')
print(subobject_mapping )