from pprint import pprint

from dataimports import sparql, file_utils
from dataimports.wikidata import wikidata


def importdata(source: str,
               outformat='stdout',
               outfile=''):

    # mapping = file_utils.yaml_get_mapping(mapping=source)

    if source == 'wikidata':
        results = sparql.query(source='wikidata',
                               query_='EventSeries')
        # print(json.dumps(results))
        for entry in results:
            pprint(entry)
            entry_simple_dict = wikidata.sparqlitem2dict(item=entry)
            pprint(entry_simple_dict)
            print('\n')

        print('Results returned:', len(results))