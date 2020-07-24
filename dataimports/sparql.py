from typing import Dict
from SPARQLWrapper import SPARQLWrapper, JSON
from dataimports.globals import useragent
from dataimports import file_utils


def query() -> Dict:
    # TODO: make non wikidata specific
    sources_yaml = file_utils.yaml_get_source('_sources.yml')
    wikidata_yaml = sources_yaml['wikidata']
    endpoint = SPARQLWrapper(wikidata_yaml['sparqlendpoint'],
                             agent=useragent)
    sparql_f = 'wikidata/wikidata_series.rq'
    sparql_query = file_utils.relative_read_f(sparql_f)
    endpoint.setQuery(sparql_query)
    endpoint.setReturnFormat(JSON)
    results = endpoint.query().convert()
    results_bindings = results['results']['bindings']
    return results_bindings
