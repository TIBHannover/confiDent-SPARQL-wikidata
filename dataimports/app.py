from pprint import pprint
from dataimports.ingestlogic import wikidata


def importdata(source: str, outformat: str, outfile: str):
    if source == 'wikidata':
        results = wikidata.sparql()
        for entry in results :
            pprint(entry)
            print('\n')

        print('Results returned:', len(results))