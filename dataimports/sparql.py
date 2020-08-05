from typing import Dict, List
from pprint import pprint
from SPARQLWrapper import SPARQLWrapper, JSON
from dataimports.globals import useragent
from dataimports import file_utils
from dataimports.wikidata import wikidata
from dataimports.jinja_utils import render_template
from dataimports.mapping import schema2confi_map, dataitem2confid_map


def query(source: str, class_: str) -> Dict:
    sources_yaml = file_utils.yaml_get_source('_sources.yml')
    source_dict = sources_yaml[source]
    sparql_endpoint = source_dict['sparqlendpoint']
    sparql_f = source_dict['sparqlqueries'][class_]
    endpoint = SPARQLWrapper(endpoint=sparql_endpoint,
                             agent=useragent)
    sparql_query = file_utils.relative_read_f(sparql_f)
    endpoint.setQuery(sparql_query)
    endpoint.setReturnFormat(JSON)
    results = endpoint.query().convert()
    results_bindings = results['results']['bindings']  # ?wikidata specific?
    return results_bindings


def process_results(results: Dict, source: str, out_format:str, class_: str):
    """
    :param results:
    :param source: wikidata
    :param out_format: wiki, dict, json
    :return:
    """
    # TODO: place properties into corresponding templates, perhaps by using
    #  class_
    # TODO: handle subobjects in template

    if source == 'wikidata':
        results = wikidata.sparqlresults_simplfy(results)
        schema_map2confi_dict = schema2confi_map(schema=source,
                                                 schema_data=results)
        for item in results:
            item_confid_keys = dataitem2confid_map(mapping=schema_map2confi_dict,
                                                   item_data=item, )

            print('item_confid_keys:', item_confid_keys)
            if out_format == 'dict':
                output = item_confid_keys
            elif out_format == 'wiki':
                output = render_template(class_=class_, item=item_confid_keys)
                # TODO: * create item title: either simply through the itemLabel
            yield output
