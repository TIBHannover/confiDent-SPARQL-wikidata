from dataimports.file_utils import yaml_get_source
from dataimports.mapping import invert_mapping
from dataimports.globals import (confid_mapping,
                                 invert_confid_map,)


def populateglobals():
    confid_mapping.update(yaml_get_source('wikidata/confident_mapping.yml'))
    invert_confid_map.update(invert_mapping(schema='wikidata'))
