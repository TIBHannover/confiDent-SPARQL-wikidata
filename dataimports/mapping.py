from typing import Dict, List
from pprint import pprint
from dataimports import file_utils


def schema2confi_map(schema: str, schema_data: List) -> Dict:
    """
    Inverts the {schema}/confident_mapping.yml
    confident_key: {'property': schema_key} -> {schema_key: confident_key}
    :schema: the external schema ie. wikidata, openresearch, etc
    :schema_data:  dict with an item's results from the external source
    :return: mapping_schema2confident
    """
    mapping_schema2confident = {}
    confident_mapping = file_utils.yaml_get_source(
        f'{schema}/confident_mapping.yml')
    for schema_data_item in schema_data:
        for extschema_k in schema_data_item:
            if extschema_k not in mapping_schema2confident:
                for confid_k, confid_dict in confident_mapping.items():
                    if confid_dict and extschema_k in confid_dict['property']:
                        mapping_schema2confident[extschema_k] = confid_k
                        break
    return mapping_schema2confident


def dataitem2confid_map(mapping: Dict, item_data: Dict) -> Dict:
    """
    Puts item property + data into confIDent properties
    :mapping: {external_property: confIDent_property, ...}
    :item_data:
    :return:
    """
    item_confid = {}
    for data_k, data_v in item_data.items():
        if data_k in mapping:
            confid_k = mapping[data_k]
            item_confid[confid_k] = data_v
    return item_confid

