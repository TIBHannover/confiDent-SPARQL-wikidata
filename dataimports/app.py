from time import sleep
from typing import Iterator, Dict
from itertools import count
from mediawikitools.wiki import actions as mwactions
from dataimports import sparql
from dataimports.file_utils import createglobals, yaml_get_source
from dataimports.wikidata import wikidata


def is_empty(generator):
    for item in generator:
        return False
    return True


def aggregate_results(results: Iterator[Dict]) -> Dict:
    aggregated_results = {}
    for result in results:
        simplified_result = wikidata.sparqlresults_simplify(dataitem=result)
        s_key = simplified_result['item'][0]
        if s_key not in aggregated_results.keys():
            aggregated_results[s_key] = simplified_result
        else:
            aggregated_results[s_key] = sparql.append_nonpresent_vals(
                srcdict=simplified_result, destdict=aggregated_results[s_key])
    return aggregated_results


def loop_sparql_results(source: str, class_: str, outformat: str,
                        limit: int, write: bool):
    aggregated_results = {}
    if limit and limit < 50:
        print(f'limit: {limit}')
        sparql_limit = limit
        # preform query in 1 go
        query_results_gen = sparql.query(source=source,
                                         class_=class_,
                                         limit=sparql_limit,
                                         offset=0)
        aggregated_results.update(aggregate_results(results=query_results_gen))
    else:
        sparql_limit = 50
        # preform query in in a iterations
        # until limit of results is reached
        # or no more results are returned
        for index in count():
            if limit and (index * sparql_limit) > limit:
                print(f'index: {index}')
                break
            sparql_offset = sparql_limit * index
            query_results_gen = sparql.query(source=source,
                                             class_=class_,
                                             limit=sparql_limit,
                                             offset=sparql_offset)
            if is_empty(generator=query_results_gen):
                break
            aggregated_results.update(
                aggregate_results(results=query_results_gen))

    for result_title, result_formatted in sparql.process_results(
            results=aggregated_results, source=source, out_format=outformat,
            class_=class_):
        print(result_title)
        if outformat == 'wiki' and write:
            sleep(4)
            wiki_page_content = (mwactions.read(page=result_title))[0]
            if result_formatted != wiki_page_content:
                mwactions.edit(page=result_title,
                               content=result_formatted,
                               newpageonly=False,
                               summary="Edited by confIDent Data Importer")
        else:
            print(result_formatted)

    return f'Source:{source} class:{class_}' \
           f'results aggregated into {len(aggregated_results)} items.'


def importdata(source: str, outformat: str, outfile: str, limit: int,
               write: bool):
    sources_yaml = yaml_get_source('_sources.yml')
    source_dict = sources_yaml[source]

    if source == 'wikidata':
        createglobals(source='wikidata')
        for query_class in source_dict['sparqlqueries'].keys():
            if 'Test' not in query_class:
                summary = loop_sparql_results(source='wikidata',
                                              class_=query_class,
                                              outformat=outformat,
                                              limit=limit,
                                              write=write)
                print(summary)
