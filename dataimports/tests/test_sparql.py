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
        results = sparql.query(source=source,
                               class_='EventSeries')
        # results_keys = results.keys()
        assert type(results) is list and len(results) > 0
        first_result = results[0]
        assert type(first_result) is dict and len(first_result.keys()) > 0