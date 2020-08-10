# from pprint import pprint
from dataimports import sparql
from dataimports.globals import (confid_mapping,
                                 invert_confid_map,
                                 )
from dataimports.file_utils import yaml_get_source
from dataimports.mapping import (invert_mapping,
                                 getall_confid_ranges,
                                 )


def importdata(source: str, outformat: str, outfile: str, limit: int):
    outfile = outfile
    # mapping = file_utils.yaml_get_mapping(mapping=source)

    if source == 'wikidata':
        # globals
        confid_mapping.update(
            yaml_get_source(f'{source}/confident_mapping.yml'))
        invert_confid_map.update(invert_mapping(schema='wikidata'))
        confid_allranges = getall_confid_ranges()
        print(confid_allranges)
        # print('schema_inv_map')
        # pprint(invert_confid_map)
        for i, result in enumerate(
                iterable=sparql.query(source='wikidata', class_='EventSeries'),
                start=1):
            if i > limit:
                break
            # print('\n', '**SPARL result:**', type(result))
            # pprint(result)
            result_formatted = sparql.process_result(dataitem=result,
                                                     source='wikidata',
                                                     out_format=outformat,
                                                     class_='EventSeries')
            current_result_i = i
            print(result_formatted)

        print(f'Results returned: {current_result_i}')
