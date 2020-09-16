from typing import List, Dict
from datetime import datetime


def sparqlresults_simplify(dataitem: Dict) -> List:
    """
    Converts the dataitem, from a sparql query to wikidata, into a
    simpliefied dict
    * dateTime is is convert to python datetime objects
    * decimals to ints

    TODO: group event_interval (int) and event_interval_unit (string ie. year)
    """
    keyvalue_dict = {}
    for k, v in dataitem.items():
        value = (v['value'].split('@@@'))[0]
        if value:
            if v.get('datatype') == \
                    'http://www.w3.org/2001/XMLSchema#dateTime':
                keyvalue_dict[k] = [
                    datetime.strptime(value, "%Y-%m-%dT%H:%M:%S%z")]
            elif v.get(
                    'datatype') == 'http://www.w3.org/2001/XMLSchema#decimal':
                keyvalue_dict[k] = [int(value)]
            else:
                keyvalue_dict[k] = [value]
    return keyvalue_dict
