import pytest
from dataimports.file_utils import yaml_get_source
from dataimports.mapping import invert_mapping


@pytest.fixture(scope="session")
def mappings():
    def _getmapping(mapping):
        confid_mapping = yaml_get_source(f'{mapping}/confident_mapping.yml')
        invert_confid_map = invert_mapping(schema=mapping)
        return confid_mapping, invert_confid_map
    return _getmapping


@pytest.fixture(scope="module")
def foo():
    def _method():
        return 10
    return _method