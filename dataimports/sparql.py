from typing import Dict
from SPARQLWrapper import SPARQLWrapper, JSON
from dataimports.globals import useragent
from dataimports import file_utils


def query(source: str, query_: str) -> Dict:
    sources_yaml = file_utils.yaml_get_source('_sources.yml')
    source_dict = sources_yaml[source]
    sparql_endpoint = source_dict['sparqlendpoint']
    sparql_f = source_dict['sparqlqueries'][query_]
    endpoint = SPARQLWrapper(endpoint=sparql_endpoint,
                             agent=useragent)
    sparql_query = file_utils.relative_read_f(sparql_f)
    endpoint.setQuery(sparql_query)
    endpoint.setReturnFormat(JSON)
    results = endpoint.query().convert()
    results_bindings = results['results']['bindings']  # ?wikidata specific?
    return results_bindings
