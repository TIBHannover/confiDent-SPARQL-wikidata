import sys
from typing import Dict, List
from dataimports.globals import confid_mapping
from dataimports.jinja_utils import render_template


classes_templates = {
    'Agent': [],
    'Contributor': [],
    'RoleAgent': [],
    'Event': ['Event', 'BFO_0000015'],
    'EventSeries': ['EventSeries', 'BFO_0000015'],
    'Group_of_Agents': [],
    'Imported_vocabulary': [],
    'Organization': [],
    'Organizer': [],
    'Person': [],
    'BFO_0000015': ['BFO_0000015'],
    'Role': [],
}


def temple4property(prop: str, class_templates: List) -> str:
    # in the context of this class_ and the property domain
    # what template shall be used?
    prop_domain = prop['domain']
    if type(prop_domain) is str:
        template = prop_domain
    else:
        print('Handling list of domains to template missing')
        # TODO:
        # # assumes there is only 1 intersection
        # template = list(set(prop_domain).intersection(class_templates))[0]
        sys.exit()
    return template


def assign_props2templates(dataitem: Dict, class_=str) -> Dict:
    """
    Since confiDent properties have different rdfs:domain,
    And more than 1 template can be used to describe a subject.
    We need to assign each properity:value to the correct templates
    We'll use key:property in confident2wikidata_mapping.yml to do handle it
    And classes_templates dict to determine what templates a class uses
    # TODO: classes_templates should be created from wiki templates with
    # property Template4Class::
    :param dataitem:
    :return:
    """
    thisclass_templates = classes_templates[class_]
    thisclass_templates_dict = {template: {} for template in
                                thisclass_templates}
    for dataitem_prop, val in dataitem.items():
        confid_prop_info = confid_mapping[dataitem_prop]
        usetemplate = temple4property(prop=confid_prop_info,
                                      class_templates=thisclass_templates)
        thisclass_templates_dict[usetemplate].update({dataitem_prop: val})
    # pprint(thisclass_templates_dict)
    return thisclass_templates_dict


def seperate_subobjects(dataitem: Dict):
    """
    Creates 2 dictictionariess of from dataitem properties:values
    * dataitem_nosubobj for properties w/out subobject
    * dataitem_subobj for properties w/ subobject
    So that they can be handled by different Jinja templates
    :param dataitem:
    :return: dataitem_nosubobj, dataitem_nosubobj

    dataitem_nosubobj structure:
        {'WDQID': 'http://www.wikidata.org/entity/Q98073704',
        'Website': 'https://link.springer.com/conference/lata'}

    dataitem_subobj structure:
        {'official_name':
            {'prop': 'Process Name'
            'val': 'International conference on language',
            'child_prop_vals': [['Process Name Type', 'official name']],
            'subobject': 'Subobject Process Name'}
        }
    """
    dataitem_nosubobj = {}
    dataitem_subobj = {}

    for dataitem_prop, val in dataitem.items():
        confid_prop = confid_mapping[dataitem_prop]
        if 'subobject' in confid_prop.keys():
            dataitem_subobj[dataitem_prop] = {
                'child_prop': confid_prop['child_prop'],
                'val': val,
                'child_prop_vals': confid_prop['child_prop_vals'],
                'subobject': confid_prop['subobject']}
            # supplement dataitem_subobj w/ confid_prop's child_prop_vals &
            # subobject. They will be necessary in the Jinja template
        else:
            dataitem_nosubobj[dataitem_prop] = val
    return dataitem_nosubobj, dataitem_subobj


def islist(value) -> bool:
    if isinstance(value, list):
        return True
    else:
        return False


def dataitem2wikipage(dataitem: Dict, class_: str) -> str:
    dataitem_nosubobj, dataitem_subobj = seperate_subobjects(
        dataitem=dataitem)
    dataitem_props_bytemplate = assign_props2templates(
        dataitem=dataitem_nosubobj, class_=class_)
    output = ''
    for template, dataitem_props in dataitem_props_bytemplate.items():
        output += render_template(mw_template=template,
                                  item=dataitem_props) + '\n'
    output += render_template(mw_template=class_,
                              item=dataitem_subobj,
                              subobjs=True)
    return output
