from SPARQLWrapper import SPARQLWrapper, JSON  # , TURTLE, RDF
from typing import Dict
from datetime import datetime
from dataimports.globals import useragent
from dataimports.utilities import file_utils


def sparql() -> Dict:
    sources_yaml = file_utils.yaml_get_source('../datasources/sources.yml')
    wikidata_yaml = sources_yaml['wikidata']
    endpoint = SPARQLWrapper(wikidata_yaml['sparqlendpoint'],
                             agent=useragent)
    sparql_f = '../sparql/wikidata_series.rq'
    sparql_query = file_utils.relative_read_f(sparql_f)
    endpoint.setQuery(sparql_query)
    endpoint.setReturnFormat(JSON)
    results = endpoint.query().convert()
    results_bindings = results['results']['bindings']
    return results_bindings


def sparqlitem2dict(item: Dict) -> Dict:
    """
    Converts a sparql item to a simpliefied dict
    with only the value and not the uri
    * dateTime is is convert to python datetime objects
    * decimals to ints

    TODO: group event_interval (int) and event_interval_unit (string ie. yeadr)
    """
    keyvalue_dict = {}
    for k, v in item.items():
        if v.get('datatype') == 'http://www.w3.org/2001/XMLSchema#dateTime':
            keyvalue_dict[k] = datetime.strptime(v['value'],
                                                 "%Y-%m-%dT%H:%M:%S%z")
        elif v.get('datatype') == 'http://www.w3.org/2001/XMLSchema#decimal':
            keyvalue_dict[k] = int(v['value'])
        else:
            keyvalue_dict[k] = v['value']

    return keyvalue_dict
