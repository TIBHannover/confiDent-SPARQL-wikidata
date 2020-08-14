import pytest
from dataimports.file_utils import yaml_get_source
from dataimports.mapping import invert_mapping


@pytest.fixture(scope="session")
def mappings():
    def _getmapping(mapping):
        confid_mapping = yaml_get_source(f'{mapping}/confident_mapping.yml')
        invert_confid_map = invert_mapping(schema=mapping,
                                           _confid_mapping=confid_mapping)
        print(f'invert_confid_map: {invert_confid_map}')
        return confid_mapping, invert_confid_map
    return _getmapping


@pytest.fixture(scope="session")
def get_invert_mapping():
    def _getmapping(mapping):
        invert_confid_map = invert_mapping(schema=mapping)
        return invert_confid_map
    return _getmapping


@pytest.fixture(scope="function")
def onevalue():
    def _method():
        return 10
    return _method