from pprint import pprint
from dataimports import sparql
from dataimports.wikidata import wikidata


def importdata(source: str, outformat: str, outfile: str):

    # mapping = file_utils.yaml_get_mapping(mapping=source)

    if source == 'wikidata':
        results = sparql.query(source='wikidata',
                               class_='EventSeries')
        print('**SPARL results: 1 item:**' )
        pprint(results[0])
        for item in sparql.process_results(results=results,
                                           source='wikidata',
                                           out_format=outformat,
                                           class_='EventSeries'):
            print('item:', item)


        # print(json.dumps(results))


        print('Results returned:', len(results))