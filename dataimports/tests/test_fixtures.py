import pytest


@pytest.mark.fixtures
def test_onevalue(onevalue):
    bar = onevalue()
    # confid_mapping = mappings_wikidata()
    assert bar == 10
    bar = 11


@pytest.mark.fixtures
def test_onevalueagain(onevalue):
    bar = onevalue()
    assert bar == 10


@pytest.mark.fixtures
def test_mappingfixture(mappings, appglobals):
    appglobals()
    confid_mapping, invert_confid_map = mappings('wikidata')
    assert len(confid_mapping) > 0
    assert len(invert_confid_map) > 0
    invert_confid_map = {}
    assert len(invert_confid_map) == 0


@pytest.mark.fixtures
def test_mappingfixtureagain(mappings, appglobals):
    appglobals()
    confid_mapping, invert_confid_map = mappings('wikidata')
    assert len(confid_mapping) > 0
    assert len(invert_confid_map) > 0
