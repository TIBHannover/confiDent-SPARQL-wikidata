# from pprint import pprint
from mediawikitools.wiki import actions as mwactions
from dataimports import sparql
from dataimports.globals import (confid_mapping,
                                 invert_confid_map,
                                 )
from dataimports.file_utils import yaml_get_source
from dataimports.mapping import (invert_mapping,
                                 # getall_confid_ranges,
                                 )


def createglobals(source='wikidata'):
    confid_mapping.update(yaml_get_source(f'{source}/confident_mapping.yml'))
    invert_confid_map.update(invert_mapping(schema=source))


def importdata(source: str, outformat: str, outfile: str, limit: int,
               write: bool):
    outfile = outfile
    # mapping = file_utils.yaml_get_mapping(mapping=source)

    if source == 'wikidata':
        createglobals(source='wikidata')
        for i, result in enumerate(
                iterable=sparql.query(source='wikidata',
                                      class_='Event_Series'),
                start=1):
            if limit and i > limit:
                break
            # print('\n', '**SPARL result:**', type(result))
            # pprint(result)
            result_title, result_formatted = sparql.process_result(
                dataitem=result,
                source='wikidata',
                out_format=outformat,
                class_='Event_Series')  # TODO: class_ come from _source.yml

            current_result_i = i
            if outformat == 'wiki' and write:
                mwactions.edit(page=result_title,
                               content=result_formatted + '[[Category:Test]]',
                               newpageonly=False,
                               summary="Edited by confIDent Data Importer")
            else:
                print(result_formatted)

        print(f'Results returned: {current_result_i}')
