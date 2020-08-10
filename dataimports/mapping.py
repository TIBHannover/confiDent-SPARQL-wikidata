from typing import Dict, List
from pprint import pprint
from dataimports.file_utils import yaml_get_source
from dataimports.globals import invert_confid_map


def invert_mapping(schema: str) -> Dict:
    """
    Inverts the {schema}/confident_mapping.yml
    confident_inv_map: {'property': schema_key} -> {schema_key: confident_key}
    """
    confident_mapping = yaml_get_source(
        f'{schema}/confident_mapping.yml')
    confident_inv_map = {}
    for k, v in confident_mapping.items():
        if v and v['external_prop']:
            prop = v['external_prop']
            if prop not in confident_inv_map.keys():
                confident_inv_map[prop] = k
    return confident_inv_map

# TODO: REMOVE
# def schema2confi_map(schema: str, schema_data: List) -> Dict:
#     """
#     Inverts the {schema}/confident_mapping.yml
#     confident_key: {'property': schema_key} -> {schema_key: confident_key}
#     :schema: the external schema ie. wikidata, openresearch, etc
#     :schema_data:  dict with an item's results from the external source
#     :return: mapping_schema2confident
#     """
#     mapping_schema2confident = {}
#     confident_mapping = file_utils.yaml_get_source(
#         f'{schema}/confident_mapping.yml')
#     for schema_data_item in schema_data:
#         for extschema_k in schema_data_item:
#             if extschema_k not in mapping_schema2confident:
#                 for confid_k, confid_dict in confident_mapping.items():
#                     if confid_dict and extschema_k in \
#                             confid_dict['external_prop']:
#                         mapping_schema2confident[extschema_k] = confid_k
#                         break
#     return mapping_schema2confident


def dataitem2confid_map(item_data: Dict) -> Dict:
    """
    Puts the item's  external_property:value value into confIDent_prop:value
    :item_data: {external_property:value, ...} result from external source query
    :return: {confid_property:value, ...}
    """
    item_confid = {}
    for data_k, data_v in item_data.items():
        if data_k in invert_confid_map:
            confid_k = invert_confid_map[data_k]
            item_confid[confid_k] = data_v
    return item_confid
