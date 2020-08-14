import pytest
from dataimports.mapping import dataitem2confid_map


@pytest.fixture()
def onesparqlresut():
    result = {
        'Twitter_username': {'type': 'literal', 'value': 'swibcon'},
        'dateModified': {
            'datatype': 'http://www.w3.org/2001/XMLSchema#dateTime',
            'type': 'literal', 'value': '2020-07-04T09:34:49Z'},
        'event_interval': {
            'datatype': 'http://www.w3.org/2001/XMLSchema#decimal',
            'type': 'literal', 'value': '1'},
        'event_interval_unitLabel': {'type': 'literal', 'value': 'year'},
        'item': {'type': 'uri',
                 'value': 'http://www.wikidata.org/entity/Q29129469'},
        'itemLabel': {'type': 'literal',
                      'value': 'Semantic Web in Libraries Conference',
                      'xml:lang': 'en'},
        'locationLabel': {'type': 'literal', 'value': 'Hamburg',
                          'xml:lang': 'en'},
        'official_website': {'type': 'uri', 'value': 'http://swib.org'},
        'short_nameLabel': {'type': 'literal', 'value': 'SWIB'},
        'NonMatchingKey': {'type': 'literal', 'value': 'FOO'}}
    return result


@pytest.mark.processing
def test_dataitem2confid_map(onesparqlresut):
    dataitem_confid_format = dataitem2confid_map(item_data=onesparqlresut)
    assert dataitem_confid_format
    assert dataitem_confid_format['acronym']['value'] == 'SWIB'


# if i can create a fixture with the results of the sparql query
    # assert that dataitem_confid_format['official_name']
    # assert that each dataitem_confid_format.keys() in confident_mapping.yml
    # key
