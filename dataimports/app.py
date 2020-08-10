from pprint import pprint
from dataimports import sparql
from dataimports.globals import invert_confid_map
from dataimports.mapping import invert_mapping


def importdata(source: str, outformat: str, outfile: str):
    outfile = outfile
    # mapping = file_utils.yaml_get_mapping(mapping=source)

    if source == 'wikidata':
        schema_inv_map = invert_mapping(schema='wikidata')
        invert_confid_map.update(schema_inv_map)  # global
        # TODO: tests

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
