from typing import Dict, Any, Union
from pprint import pprint
from dataimports import sparql
from dataimports.wikidata import wikidata


def simplify_result(dataitem: Dict, source: str, out_format: str, class_: str)\
        -> [str, Any]:
    if source == 'wikidata':
        dataitem = wikidata.sparqlresults_simplfy(dataitem=dataitem)
    return dataitem


def append_nonpresent_vals(srcdict: Dict, destdict: Dict) -> Dict:
    for srcdict_k, srcdict_v in srcdict.items():
        if srcdict_v[0] not in destdict[srcdict_k]:
            destdict[srcdict_k].append(srcdict_v[0])
    return destdict


aggregated_results = {}

for i, result in enumerate(sparql.query(source='wikidata',
                                     class_='Test_Repeated_Items')):
    simplified_result = simplify_result(dataitem=result,
                                       source='wikidata',
                                       out_format='dict',
                                       class_='Test_Repeated_Items')
    simplified_key = simplified_result['item'][0]
    if simplified_key not in aggregated_results.keys():
        aggregated_results[simplified_key] = simplified_result
    else:
        aggregated_results[simplified_key] = append_nonpresent_vals(
            srcdict=simplified_result,
            destdict=aggregated_results[simplified_key])
    print(simplified_result, type(simplified_result))
    if i > 5:
        break
pprint(aggregated_results)
"""
{'http://www.wikidata.org/entity/Q48619834': 
    {'Twitter_username': ['acl2018'],
    'countryLabel': ['Australia'],
    'item': ['http://www.wikidata.org/entity/Q48619834'],
    'language_usedLabel': ['English'],
    'main_subjectLabel': ['computational '
                        'linguistics'],
    'official_website': ['http://acl2018.org'],
    'organizerLabel': ['Iryna '
                     'Gurevych'],
    'short_name': ['ACL 2018']},
 'http://www.wikidata.org/entity/Q64955764': 
    {'Twitter_username': ['ecir2020'],
      'countryLabel': ['Portugal'],
      'item': ['http://www.wikidata.org/entity/Q64955764'],
      'language_usedLabel': ['English'],
      'main_subjectLabel': ['information '
                            'retrieval'],
      'official_website': ['https://ecir2020.org/'],
      'organizerLabel': ['Christina '
                         'Lioma',
                         'Nuno Correia',
                         'Suzan '
                         'Verberne',
                         'Nicola '
                         'Ferro'],
      'short_name': ['ECIR 2020']},
 'http://www.wikidata.org/entity/Q72838890': 
     {'Twitter_username': ['coling2020'],
      'countryLabel': ['Spain'],
      'item': ['http://www.wikidata.org/entity/Q72838890'],
      'language_usedLabel': ['English'],
      'main_subjectLabel': ['computational '
                            'linguistics'],
      'official_website': ['https://coling2020.org/'],
      'organizerLabel': ['Horacio '
                         'Saggion',
                         'Leo Wanner'],
      'short_name': ["COLING'2020"]}
}
