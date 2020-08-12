from typing import Dict, List
from dataimports.globals import confid_mapping


classes_templates = {
    'Agent': [],
    'Contributor': [],
    'RoleAgent': [],
    'Event': ['Event', 'Process'],
    'Event_Series': ['Event_Series', 'Process'],
    'Group_of_Agents': [],
    'Imported_vocabulary': [],
    'Organization': [],
    'Organizer': [],
    'Person': [],
    'Process': [],
    'Role': [],
}


def temple4property(prop: str, class_templates: List) -> str:
    # in the context of this class_ and the property domain
    # what template shall be used?
    prop_domain = prop['domain']
    # assumes there is only 1 intersection
    template = list(set(prop_domain).intersection(class_templates))[0]
    return template


def assign_props2templates(dataitem: Dict, class_=str) -> Dict:
    """
    Since confiDent properties have different rdfs:domain,
    And more than 1 template can be used to describe a subject.
    We need to assign each properity:value to the correct templates
    We'll use key:property in confident_mapping.yml to do handle it
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
