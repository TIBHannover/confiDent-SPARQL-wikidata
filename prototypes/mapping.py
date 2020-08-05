from pprint import pprint

confident_map = {
    'Website': {
        'property': 'official_website',
        'URI': 'https://www.wikidata.org/wiki/Property:P856'
    },
     'Twitter': {
         'property': 'Twitter_username',
         'URI': 'https://www.wikidata.org/wiki/Property:P2002'
         }
}

# challenge 1: invert dictionary


def invert_dict(srcdict):
    destdict = {}
    for k, v in srcdict.items():
        prop = v['property']
        if prop not in destdict.keys():
            destdict[prop] = k
    return destdict

inverted_confid_map = invert_dict(confident_map)
print(inverted_confid_map)

# challenge 2: structure for subobject:
# there is MORE THAN 1 PROPERTY per semantic suboject "cluster":
#   ie Process Name, Process Name Type
# there is a hierarchy between the propertyes
#   * Process Name:
#        * Process Name Type
# the value of child property determines to which exte. property it
#   will be mapped to
# the properties will be same for the different instances of a subobject
# the subobject is identified by its template name

confident_map_subobjts = {
    'Process Name-official name': {
        'property': 'official name',
        'child_prop_vals': [('Process Name Type', 'official name')]
    },
    'Process Name-acronym': {
        'property': 'short name',
        'child_prop_vals': [('Process Name Type', 'official name')]
    },
}

confident_map.update(confident_map_subobjts)
pprint(confident_map)


def invert_dict(srcdict):
    destdict = {}
    for k, v in srcdict.items():
        keys = v.keys()
        prop = v['property']
        if prop not in destdict.keys():
            destdict[prop] = k
        else:
            prop = v['property']
            if prop not in destdict.keys():
                destdict[prop] = k
    return destdict

inverted_confid_map = invert_dict(confident_map)
print(inverted_confid_map)

# {'Twitter_username': 'Twitter',
# 'official  name': 'Process Name-official
# name', 'short name': 'Process Name-acronym'}
# keys are correct

'''
{{Subobject Process Name
|Process Name=PIDapalooza 2020
|Process Name Type=official name
}}

acronym=XYZ (1 prop wikidata
 \|/
Process Name Type=acronym  (2 prop confIDent
Process Name=XYZ

{{Subobject Process Name
|Process Name=PID(test)
|Process Name Type=acronym
}}
'''