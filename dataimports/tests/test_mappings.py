import pytest
from dataimports.file_utils import yaml_get_source
from dataimports.mapping import invert_mapping
from dataimports.globals import (confid_mapping,
                                 invert_confid_map,
                                 )

# TODO: Test for integraty of confident_mapping.yml

@pytest.mark.mapping
def test_confid_mapping():
    sources = ['wikidata']
    for schema in sources:
        confid_mapping.update(
            yaml_get_source(f'{schema}/confident_mapping.yml'))
        confid_keys = list(confid_mapping.keys())
        confid_keys_set = list(set(confid_keys))

        external_props = [v['external_prop']
                          for k, v in confid_mapping.items() if
                          v and 'external_prop' in v.keys()
                          and v['external_prop']]

        assert len(external_props) > 0, \
            f"Expected mapping. {confid_mapping} is empty"

        assert sorted(confid_keys) == sorted(confid_keys_set),\
            f"Expected unique keys in mapping, Actual keys {confid_keys}"
        invert_confid_map.update(invert_mapping(schema=schema))
        print(schema, invert_confid_map)
        confid_keys_in_inv_mapping = [v for v in invert_confid_map.values()]
        assert len(invert_confid_map) > 0
        for k in confid_keys_in_inv_mapping:
            assert k in confid_keys,\
                f"confid key: {k} in inverted mapping is not in confid keys " \
                f"of {schema}"
