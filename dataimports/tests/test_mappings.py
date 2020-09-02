import pytest
from pathlib import Path
from dataimports.file_utils import yaml_get_source


@pytest.mark.mapping
def test_mapping_files(find_files):
    mappingfiles = find_files(filename='confident_mapping.yml',
                              startdir='dataimports',
                              foundfiles=[])
    assert len(mappingfiles) > 0
    for mappingfile_path in mappingfiles:
        file_ = Path(mappingfile_path).parent.name / Path(
            Path(mappingfile_path).name)
        mapping = yaml_get_source(file_)
        assert type(mapping) is dict
        for mapping_k, mapping_val in mapping.items():
            assert 'external_props' in mapping_val.keys()
            assert type(mapping_val['external_props']) is list
            assert type(mapping_val['external_props'][0]) is dict
            assert 'URI' in mapping_val['external_props'][0].keys()
            assert 'external_prop' in mapping_val['external_props'][0].keys()

            assert mapping_val['domain']
            if 'subobject' in mapping_val.keys():
                assert mapping_val['child_prop']
                assert type(mapping_val['child_prop_vals']) is list


@pytest.mark.mapping
def test_confid_mapping(mappings):
    schema = 'wikidata'
    confid_mapping, invert_confid_map = mappings(schema)
    assert len(invert_confid_map) > 0
    confid_mapping.update(
        yaml_get_source(f'{schema}/confident_mapping.yml'))
    confid_keys = list(confid_mapping.keys())
    confid_keys_set = list(set(confid_keys))
    external_props = [v['external_props']
                      for k, v in confid_mapping.items() if
                      v and 'external_props' in v.keys()
                      and v['external_props']]
    assert len(external_props) > 0, \
        f"Expected mapping. {confid_mapping} is empty"
    assert all([isinstance(prop_tup, list) for prop_tup in external_props])
    assert all([isinstance(prop_tup[0], dict) for prop_tup in external_props])
    assert sorted(confid_keys) == sorted(confid_keys_set),\
        f"Expected unique keys in mapping, Actual keys {confid_keys}"
    confid_keys_in_inv_mapping = [v for v in invert_confid_map.values()]
    for k in confid_keys_in_inv_mapping:
        assert k in confid_keys,\
            f"confid key: {k} in inverted mapping is not in confid keys " \
            f"of {schema}"


@pytest.mark.mapping
def test_confid_mapping_yaml(mappings):
    schema = 'wikidata'
    confid_mapping, invert_confid_map = mappings('wikidata')
    confid_mapping.clear()  # reset dict for each source
    confid_mapping.update(
        yaml_get_source(f'{schema}/confident_mapping.yml'))
    for k, value_dict in confid_mapping.items():
        assert 'domain' in value_dict, \
            f"domain: is missing from {schema}/confident_mapping.yml " \
            f"key: {k}"
