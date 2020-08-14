import pytest
from dataimports.mapping import dataitem2confid_map


@pytest.mark.processing
def test_dataitem2confid_map(onesparqlresut, mappings):
    sparql_result_dict = onesparqlresut()
    assert len(sparql_result_dict) > 0
    confid_mapping, invert_confid_map = mappings('wikidata')
    dataitem_confid_format = dataitem2confid_map(
        item_data=sparql_result_dict,
        _invert_confid_map=invert_confid_map)
    assert len(dataitem_confid_format) > 0
    assert dataitem_confid_format['acronym']['value'] == 'SWIB'


# if i can create a fixture with the results of the sparql query
    # assert that dataitem_confid_format['official_name']
    # assert that each dataitem_confid_format.keys() in confident_mapping.yml
    # key
