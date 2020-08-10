from typing import List, Dict
from datetime import datetime


def sparqlresults_simplfy(results: Dict) -> List:
    """
    Converts the results' items, from a sparql query to wikidata, into a
    list of simpliefied dicts, with only the value
    * dateTime is is convert to python datetime objects
    * decimals to ints

    TODO: group event_interval (int) and event_interval_unit (string ie. year)
    """
    results_new = []
    for item in results:
        keyvalue_dict = {}
        for k, v in item.items():
            if v.get('datatype') == \
                    'http://www.w3.org/2001/XMLSchema#dateTime':
                keyvalue_dict[k] = datetime.strptime(v['value'],
                                                     "%Y-%m-%dT%H:%M:%S%z")
            elif v.get(
                    'datatype') == 'http://www.w3.org/2001/XMLSchema#decimal':
                keyvalue_dict[k] = int(v['value'])
            else:
                keyvalue_dict[k] = v['value']
        results_new.append(keyvalue_dict)
    return results_new
