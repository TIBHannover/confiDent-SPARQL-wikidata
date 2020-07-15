from SPARQLWrapper import SPARQLWrapper, JSON  # , TURTLE, RDF
from typing import Dict
from dataimports.utilities import file_utils


def sparql() -> Dict:
    sources_yaml = file_utils.yaml_get_source('../datasources/sources.yml')
    wikidata_yaml = sources_yaml['wikidata']
    endpoint = SPARQLWrapper(wikidata_yaml['sparqlendpoint'])
    sparql_f = '../sparql/wikidata_series.rq'
    sparql_query = file_utils.relative_read_f(sparql_f)
    endpoint.setQuery(sparql_query)
    endpoint.setReturnFormat(JSON)
    results = endpoint.query().convert()
    results_bindings = results['results']['bindings']
    return results_bindings
