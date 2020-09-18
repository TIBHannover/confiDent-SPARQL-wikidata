from time import sleep
from mediawikitools.wiki import actions as mwactions
from dataimports import sparql
from dataimports.file_utils import createglobals, yaml_get_source
from dataimports.wikidata import wikidata


def is_empty(generator):
    for item in generator:
        return False
    return True

def loop_sparql_results(source: str, class_: str, outformat: str,
                        limit: int, write: bool):
    aggregated_results = {}
    for index in range(1000):  # 50000 items is a safe bet
        limit = 50
        offset = limit * index
        query_results_gen = sparql.query(source=source, class_=class_,
                                         limit=limit, offset=offset)
        sleep(1)
        if is_empty(query_results_gen):
            break

        for i, result in enumerate(iterable=query_results_gen, start=1):
            # if limit and i > limit:
            #     break
            # print('\n', '**SPARL result:**', type(result))
            # pprint(result)
            simplified_result = wikidata.sparqlresults_simplify(dataitem=result)
            s_key = simplified_result['item'][0]
            if s_key not in aggregated_results.keys():
                aggregated_results[s_key] = simplified_result
            else:
                aggregated_results[s_key] = sparql.append_nonpresent_vals(
                    srcdict=simplified_result, destdict=aggregated_results[s_key])
            current_result_i = i  # TODO: test aggregated_results

    for result_title, result_formatted in sparql.process_results(
            results=aggregated_results, source=source, out_format=outformat,
            class_=class_):
        print(result_title)

        if outformat == 'wiki' and write:
            sleep(4)
            mwactions.edit(page=result_title,
                           content=result_formatted,
                           newpageonly=False,
                           summary="Edited by confIDent Data Importer")
        else:
            print(result_formatted)

    return f'Source:{source} class:{class_} returned:{current_result_i} ' \
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
