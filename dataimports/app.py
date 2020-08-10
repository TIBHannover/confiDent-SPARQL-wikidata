from pprint import pprint
from dataimports import sparql
from dataimports.globals import (confid_mapping,
                                 invert_confid_map,
                                 )
from dataimports.file_utils import yaml_get_source
from dataimports.mapping import (invert_mapping,
                                 getall_confid_ranges,
                                 )


def importdata(source: str, outformat: str, outfile: str):
    outfile = outfile
    # mapping = file_utils.yaml_get_mapping(mapping=source)

    if source == 'wikidata':
        # globals
        confid_mapping.update(
            yaml_get_source(f'{source}/confident_mapping.yml'))
        invert_confid_map.update(invert_mapping(schema='wikidata'))
        confid_allranges = getall_confid_ranges()
        print('confid_allranges:', confid_allranges)


        print('schema_inv_map')
        pprint(invert_confid_map)
        results = sparql.query(source='wikidata',
                               class_='EventSeries')
        print('**SPARL results: 1 item:**')
        pprint(results[0])
        for item in sparql.process_results(results=results,
                                           source='wikidata',
                                           out_format=outformat,
                                           class_='EventSeries'):
            print('item:', item)

        # print(json.dumps(results))
        print('Results returned:', len(results))
