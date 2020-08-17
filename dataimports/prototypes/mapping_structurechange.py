import os
import sys
from pathlib import Path
# from ..file_utils import  yaml_get_source


def find_files_recursively(filename: str, startdir: str, foundfiles):
    for dir_or_file in os.scandir(startdir):
        if dir_or_file.is_file() and dir_or_file.name == filename:
            foundfiles.append(dir_or_file.path)
        elif dir_or_file.is_dir():
            find_files_recursively(filename=filename,
                                   startdir=dir_or_file.path,
                                   foundfiles=foundfiles)
    return foundfiles

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
    from dataimports.file_utils import yaml_get_source, dict2yaml

    mappingfiles = find_files_recursively(filename='confident_mapping.yml',
                                          startdir='dataimports',
                                          foundfiles=[])
    mappingfile_path = mappingfiles[0]
    file_ = Path(mappingfile_path).parent.name / Path(
        Path(mappingfile_path).name)

    mapping = yaml_get_source(file_)
    for confi_prop, prop_dict in mapping.items():
        # print(confi_prop, prop_dict)
        # confi_prop['external_prop']
        # external_prop_dict = prop_dict['external_prop']

        # keep values
        if prop_dict['external_prop']:
            external_prop_val = prop_dict['external_prop']
            external_prop_URI = prop_dict['URI']
        else:
            external_prop_val = ''
            external_prop_URI = ''
            # print(external_prop_URI, external_prop_val)
        # remove old keys
        prop_dict.pop('external_prop')
        prop_dict.pop('URI')
        # create new structure with values
        prop_dict['external_props'] = [{
            'URI': external_prop_URI,
            'external_prop': external_prop_val
            }]
        # print(prop_dict)
    yaml_get_source(relativepath2f='test.yml', method='write', data=mapping)
            # confi_prop
            # assert 'external_prop' in prop_dict.keys()


# change key 'external_prop' -> 'external_props'
# get URI value
# change 'external_prop' to list of Dict
# 'external_props': [{'external_prop': val,
#                     ''URI: urival},
#                     ]