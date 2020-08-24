# from pprint import pprint
from mediawikitools.wiki import actions as mwactions
from dataimports import sparql
from dataimports.file_utils import createglobals


def loop_sparql_results(source: str, class_: str, outformat: str, outfile: str,
                        limit: int, write: bool):
    for i, result in enumerate(
            iterable=sparql.query(source=source, class_=class_),
            start=1):
        if limit and i > limit:
            break
        # print('\n', '**SPARL result:**', type(result))
        # pprint(result)
        result_title, result_formatted = sparql.process_result(
            dataitem=result, source=source, out_format=outformat,
            class_=class_)  # TODO: class_ come from _source.yml

        current_result_i = i
        if outformat == 'wiki' and write:
            mwactions.edit(page=result_title,
                           content=result_formatted + '[[Category:Test]]',
                           newpageonly=False,
                           summary="Edited by confIDent Data Importer")
        else:
            print(result_formatted)

    return f'Source:{source} class:{class_}, returned:{current_result_i} ' \
           f'results'


def importdata(source: str, outformat: str, outfile: str, limit: int,
               write: bool):
    outfile = outfile
    # mapping = file_utils.yaml_get_mapping(mapping=source)

    if source == 'wikidata':
        createglobals(source='wikidata')
        summary = loop_sparql_results(source='wikidata', class_='Event_Series',
                                      outformat=outformat, outfile=outfile,
                                      limit=limit, write=write)
        print(summary)

        summary = loop_sparql_results(source='wikidata',
                                      class_='Event',
                                      outformat=outformat, outfile=outfile,
                                      limit=limit, write=write)
        print(summary)
