import pytest
# from dataimports.mapping import dataitem2confid_map
# from dataimports.mediawiki import dataitem2wikipage
# from dataimports.mediawiki import seperate_subobjects


@pytest.mark.processing
def test_dataitem2wikioutput(onesparqlresut, mappings, appglobals):
    appglobals()
    sparql_result_dict = onesparqlresut()
    assert len(sparql_result_dict) > 0
    # confid_mapping, invert_confid_map = mappings('wikidata')
    # dataitem_confid_format = dataitem2confid_map(
    #     item_data=sparql_result_dict)
    # import pdb; pdb.set_trace()
    # assert len(dataitem_confid_format) > 0
    # assert sparql_result_dict['itemLabel']['value'] ==
    # dataitem_confid_format[
    #     'official_name']['value']
    # assert dataitem_confid_format['acronym']['value'] == 'NeurIPS'
    # output = dataitem2wikipage(dataitem=dataitem_confid_format,
    #                            class_='Event_Series')
    # assert "{{Event_Series" in output
    # assert "{{Process" in output
    # assert "{{Subobject Process Name" in output

# assert that each dataitem_confid_format.keys() in
# confident2wikidata_mapping.yml

# TODO: uncomment and run when subobjects are integrated
# @pytest.mark.processing
# def test_seperate_subobjects(one_dataitem_confikeys, appglobals):
#     appglobals()
#     dataitem = one_dataitem_confikeys()
#     dataitem_nosubobj, dataitem_subobj = seperate_subobjects(
#     dataitem=dataitem)
#     assert all([False if k in ['official_name', 'acronym'] else True for k in
#                 dataitem_nosubobj])
#     assert dataitem_nosubobj['Website']['value'] == 'http://swib.org'
#     assert len(dataitem_nosubobj) > 0 and len(dataitem_subobj) > 0
#     print(dataitem_nosubobj)
#     assert all([True if k in ['official_name', 'acronym'] else False for k in
#                 dataitem_subobj])
#     for k, subobjects in dataitem_subobj.items():
#         assert len(subobjects['child_prop_vals']) > 0 and len(subobjects[
#             'child_prop_vals'][0]) == 2
#     assert dataitem_subobj.keys()
