from typing import Dict, Any
from SPARQLWrapper import SPARQLWrapper, JSON
from dataimports.globals import useragent
from dataimports.file_utils import yaml_get_source, relative_read_f
from dataimports.wikidata import wikidata
from dataimports.mapping import dataitem2confid_map
from dataimports.mediawiki import dataitem2wikipage


def query(source: str, class_: str) -> Dict:
    sources_yaml = yaml_get_source('_sources.yml')
    source_dict = sources_yaml[source]
    sparql_endpoint = source_dict['sparqlendpoint']
    sparql_f = source_dict['sparqlqueries'][class_]
    endpoint = SPARQLWrapper(endpoint=sparql_endpoint,
                             agent=useragent)
    sparql_query = relative_read_f(sparql_f)
    endpoint.setQuery(sparql_query)
    endpoint.setReturnFormat(JSON)
    results = endpoint.query().convert()
    results_bindings = results['results']['bindings']  # ?wikidata specific?
    for result in results_bindings:
        yield result


def process_results(results: Dict, source: str, out_format: str, class_: str)\
        -> [str, Any]:
    """
    Maps the properties:value from results onto confIDent properties
    And outputs them in the form of the out_format
    :param dataitem: item printouts, from sparql query
    :param source: wikidata
    :param out_format: wiki, dict, json
    :param class_:
    :return:
    """
    # TODO: place properties into corresponding templates, perhaps by using
    #  class_
    # TODO: handle subobjects in template

    for dataitem in results.values():
        dataitem_confid_format = dataitem2confid_map(item_data=dataitem)
        title = dataitem_confid_format['official_name'][0]

        if out_format == 'dict':
            output = dataitem_confid_format
        elif out_format == 'wiki':
            output = dataitem2wikipage(dataitem=dataitem_confid_format,
                                       class_=class_)
        else:
            output = None
        yield title, output


def simplify_result(dataitem: Dict) -> [str, Any]:
    dataitem = wikidata.sparqlresults_simplfy(dataitem=dataitem)
    return dataitem


def append_nonpresent_vals(srcdict: Dict, destdict: Dict) -> Dict:
    for srcdict_k, srcdict_v in srcdict.items():
        if srcdict_v[0] not in destdict[srcdict_k]:
            destdict[srcdict_k].append(srcdict_v[0])
    return destdict
