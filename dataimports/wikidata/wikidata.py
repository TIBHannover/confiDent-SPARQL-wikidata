from typing import Dict
from datetime import datetime


def sparqlitem2dict(item: Dict) -> Dict:
    """
    Converts a query item to a simpliefied dict
    with only the value and not the uri
    * dateTime is is convert to python datetime objects
    * decimals to ints

    TODO: group event_interval (int) and event_interval_unit (string ie. yeadr)
    """
    keyvalue_dict = {}
    for k, v in item.items():
        if v.get('datatype') == 'http://www.w3.org/2001/XMLSchema#dateTime':
            keyvalue_dict[k] = datetime.strptime(v['value'],
                                                 "%Y-%m-%dT%H:%M:%S%z")
        elif v.get('datatype') == 'http://www.w3.org/2001/XMLSchema#decimal':
            keyvalue_dict[k] = int(v['value'])
        else:
            keyvalue_dict[k] = v['value']

    return keyvalue_dict
