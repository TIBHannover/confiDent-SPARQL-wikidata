import json
from pprint import pprint
from dataimports.ingestlogic import wikidata
from dataimports.utilities import file_utils


def importdata(source: str,
               outformat='stdout',
               outfile=''):

    mapping = file_utils.yaml_get_mapping(mapping=source)

    if source == 'wikidata':
        results = wikidata.sparql()
        # print(json.dumps(results))
        for entry in results:
            pprint(entry)
            entry_simple_dict = wikidata.sparqlitem2dict(item=entry)
            pprint(entry_simple_dict)
            print('\n')

        print('Results returned:', len(results))