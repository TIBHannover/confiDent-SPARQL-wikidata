from pprint import pprint
from mediawikitools.wiki import actions as mwactions
from dataimports import sparql
from dataimports.file_utils import createglobals


def importdata(source: str, outformat: str, outfile: str, limit: int,
               write: bool):
    outfile = outfile
    # mapping = file_utils.yaml_get_mapping(mapping=source)

    if source == 'wikidata':
        createglobals(source='wikidata')
        aggregated_results = {}
        for i, result in enumerate(
                iterable=sparql.query(source='wikidata',
                                      class_='Event_Series'),
                start=1):
            if limit and i > limit:
                break
            # print('\n', '**SPARL result:**', type(result))
            # pprint(result)
            simplified_result = sparql.simplify_result(dataitem=result)
            s_key = simplified_result['item'][0]
            if s_key not in aggregated_results.keys():
                aggregated_results[s_key] = simplified_result
            else:
                aggregated_results[s_key] = sparql.append_nonpresent_vals(
                    srcdict=simplified_result,
                    destdict=aggregated_results[s_key])
            current_result_i = i
            # TODO: test aggregated_results

        for result_title, result_formatted in sparql.process_results(
                results=aggregated_results,
                source='wikidata',
                out_format = outformat,
                class_='Event_Series'):
            print(result_title)

            if outformat == 'wiki' and write:
                mwactions.edit(page=result_title,
                               content=result_formatted + '[[Category:Test]]',
                               newpageonly=False,
                               summary="Edited by confIDent Data Importer")
            else:
                print(result_formatted)

        print(f'Results returned: {current_result_i}')
