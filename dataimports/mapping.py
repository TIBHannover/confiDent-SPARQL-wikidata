from typing import Dict, List
from dataimports.globals import (invert_confid_map,
                                 confid_mapping,
                                 )


def invert_mapping(schema: str) -> Dict:
    """
    Inverts the {schema}/confident2wikidata_mapping.yml
    confident_inv_map: {'property': schema_key} -> {schema_key: confident_key}
    """
    confident_inv_map = {}
    for k, v in confid_mapping.items():
        if v and v['external_props'] and \
                v['external_props'][0]['external_prop']:
            for ext_prop_dict in v['external_props']:
                prop = ext_prop_dict['external_prop']
                if prop not in confident_inv_map.keys():
                    confident_inv_map[prop] = k
    return confident_inv_map


def dataitem2confid_map(item_data: Dict) -> Dict:
    """
    Puts the item's  external_property:value value into confIDent_prop:value
    :item_data:{external_property:[value1, value2], ...}
    :return: {confid_property:[value1, value2], ...}
    """
    item_confid = {}
    for data_k, data_v in item_data.items():
        if data_k in invert_confid_map:
            confid_k = invert_confid_map[data_k]
            if not item_confid.get(confid_k):
                item_confid[confid_k] = data_v
            else:
                item_confid[confid_k] + data_v
    return item_confid


def getall_confid_ranges() -> List:
    """
    Adds all Classes uses by confIDent ontology, by looking at the
    properties' Range, to global allranges
    """
    allranges = [prop_dict.get('range') for prop_dict in
                 confid_mapping.values()]
    allranges = [i for i_list in allranges for i in i_list]  # flatten list
    allranges = list(set(allranges))
    return allranges
