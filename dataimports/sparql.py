from typing import Dict
from SPARQLWrapper import SPARQLWrapper, JSON
from dataimports.globals import useragent
from dataimports.file_utils import yaml_get_source, relative_read_f
from dataimports.wikidata import wikidata
from dataimports.jinja_utils import render_template
from dataimports.mapping import dataitem2confid_map


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
    return results_bindings


def process_results(results: Dict, source: str, out_format: str, class_: str):
    """
    :param results:
    :param source: wikidata
    :param out_format: wiki, dict, json
    :param class_:
    :return:
    """
    # TODO: place properties into corresponding templates, perhaps by using
    #  class_
    # TODO: handle subobjects in template

    if source == 'wikidata':
        results = wikidata.sparqlresults_simplfy(results)
        for item in results:
            item_confid_map = dataitem2confid_map(item_data=item)

            print('item_confid_map:', item_confid_map)
            if out_format == 'dict':
                output = item_confid_map
            elif out_format == 'wiki':
                output = render_template(class_=class_, item=item_confid_map)
                # TODO: create item title: either simply through the itemLabel
            else:
                output = None
            yield output
