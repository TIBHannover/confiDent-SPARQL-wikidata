from pprint import pprint

# todo: in yaml/dict here: replace key property external_prop external_prop_external_prop_URI

confident_map = {
    'Website': {
        'external_prop': 'official_website',
        'external_prop_URI': 'https://www.wikidata.org/wiki/Property:P856',
        'range': ['Process', 'Agent']
    },
     'Twitter': {
         'external_prop': 'Twitter_username',
         'external_prop_URI': 'https://www.wikidata.org/wiki/Property:P2002',
         'range': ['Process', 'Agent']
         },
    'Event Frequency': {
        'external_prop': 'event_interval',
        'external_prop_URI': 'https://www.wikidata.org/wiki/Property:P2257',
        'range': ['Event Series']
    }
}


def all_confid_ranges(mapdict):
    allranges = []
    for prop_dict  in mapdict.values():
        range = prop_dict.get('range')
        allranges += range
    allranges = list(set(allranges))
    return allranges


allranges = all_confid_ranges(mapdict=confident_map)


# challenge 1: invert dictionary
def invert_dict(srcdict):
    destdict = {}
    for k, v in srcdict.items():
        prop = v['external_prop']
        if prop not in destdict.keys():
            destdict[prop] = k
    return destdict


# challenge 2: structure confident_map to accommodated for subobject:
# there is MORE THAN 1 PROPERTY per semantic suboject "cluster":
#   ie Process Name, Process Name Type
# the subobject is identified by its template name

confident_map_subobjts = {
    'official name': {
        'external_prop': 'itemLabel',
        'child_prop_vals': [('Process Name Type', 'official name')],
        'subobject': 'Subobject Process Name'
    },
    'acronym': {
        'external_prop': 'short_name',
        'child_prop_vals': [('Process Name Type', 'acronym')],
        'subobject': 'Subobject Process Name'
    },
}
# not the use of propety value tuples in child_prop_vals
confident_map.update(confident_map_subobjts)
pprint(confident_map)
inverted_confid_map = invert_dict(confident_map)
print('inverted_confid_map:', inverted_confid_map)

wd_mock_data ={'official_website': 'https://nips.cc/',
               'Twitter_username': 'NeurIPSConf',
               'short_name': 'NeurIPS',
               'Freebase_ID': '/m/07rwz3',
               'event_interval': '1 year'
               }
print('data item (as captured from source - not mapped):', wd_mock_data)


# extract the values needed for confIDent properties
def dataitem2confid(datadict, inv_confid_map):
    datadict_confid = {}
    # loop through prop:val(s) from ext. data source item (datadict)
    for datadict_k, datadict_v in datadict.items():
        if datadict_k in inv_confid_map.keys():
            # from ext. data prop get corresponding confIDent property
            confid_prop = inv_confid_map[datadict_k]
            # store the external data source value, under the corresponding
            # confIDent property
            datadict_confid[confid_prop] = datadict_v
    return datadict_confid


dataitem_confid = dataitem2confid(datadict=wd_mock_data,
                                  inv_confid_map=inverted_confid_map)
print('data item mapped to confIDent:', dataitem_confid)

# when producing the output with Jinja template
# create first the none-subprocess templates
for range_ in allranges:
    print(f'-> {range_}')
    for k, v in dataitem_confid.items():
        confid_item_keys = confident_map[k].keys()
        if 'subobject' not in confid_item_keys:
            confid_item_range = confident_map[k]['range']
            if range_ in confid_item_range:
                print('range:', range_, ' / property:', k, '- val:', v)

# and then create the the process templates
for k, v in dataitem_confid.items():
    if 'subobject' in confident_map[k].keys():
        print('subobject in:', confident_map[k].keys())
        subobj_template =  confident_map[k]['subobject']
        subobj_child_propvals =  confident_map[k]['child_prop_vals']
        print(f'-> {subobj_template}')
        print(subobj_child_propvals)



