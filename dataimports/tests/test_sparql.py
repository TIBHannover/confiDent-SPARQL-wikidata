import pytest
from dataimports import sparql
from dataimports.file_utils import yaml_get_source, relative_read_f

@pytest.mark.sparql
def test_sources_file():
    srcsfile = '_sources.yml'
    sources_yaml_dict = yaml_get_source(srcsfile)
    for src, src_dict in sources_yaml_dict.items():
        assert src_dict['sparqlendpoint'] and src_dict['sparqlqueries'], \
            f'{src} misses its sparqlendpoint or sparqlqueries in {srcsfile}'

        for query_name, query_file in src_dict['sparqlqueries'].items():
            assert query_name and query_file
            sparql_query = relative_read_f(query_file)
            assert sparql_query,\
                f'No content found in {query_file}'
            #  Todo: validate query


@pytest.mark.sparql
def test_sparql_queries():
    sparql_sources = ['wikidata']
    for source in sparql_sources:
        for i, result in enumerate(
                sparql.query(source=source, class_='Event_Series')):
            if i > 20:
                break
        # results_keys = results.keys()
            assert type(result) is dict and result.keys()


@pytest.mark.sparql
def test_sparql_printouts_n_result_processing(appglobals):
    # test if the prop:value pairs from the test_wikidata_series.rq are
    # still present after the results have been processed and mapped to
    # confIDent
    appglobals()
    for i, result in enumerate(iterable=sparql.query(
            source='wikidata',
            class_='Test_Event_Series'), start=1):
        assert len(result['itemLabel']['value']) > 0
        result_title, result_formatted = sparql.process_result(
            dataitem=result,
            source='wikidata',
            out_format='dict',
            class_='Event_Series')
        print(result_title, result_formatted, '\n')
        # sparql has 4 non optional props
        assert len(result_formatted) >= 4 and result_title
        result_vals = [v['value'] for k, v in result.items()]
        result_formatted_vals = [v for v in result_formatted.values()]
        samevals = (all(str(i) in result_vals for i in result_formatted_vals))
        assert samevals is True
