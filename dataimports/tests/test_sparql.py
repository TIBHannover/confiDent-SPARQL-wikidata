import pytest
from pprint import pprint
from dataimports import sparql
from dataimports.file_utils import yaml_get_source, relative_read_f
from dataimports.wikidata import wikidata


@pytest.mark.sparql
def test_sources_file():
    srcsfile = '_sources.yml'
    sources_yaml_dict = yaml_get_source(srcsfile)
    for src, src_dict in sources_yaml_dict.items():
        assert src_dict['sparqlendpoint'] and src_dict['sparqlqueries'], \
            f'{src} misses its sparqlendpoint or sparqlqueries in {srcsfile}'

        for query_name, query_file in src_dict['sparqlqueries'].items():
            assert query_name and query_file
            sparql_query = relative_read_f(query_file)
            assert sparql_query,\
                f'No content found in {query_file}'
            #  Todo: validate query


@pytest.mark.sparql
def test_sparql_queries():
    sparql_sources = ['wikidata']
    for source in sparql_sources:
        all_results = []
        for i, result in enumerate(
                sparql.query(source=source, class_='EventSeries')):
            # if i > 20:
            #     break
            # result_keys = result.keys()
            pprint(result)
            all_results.append(result['item']['value'])
            assert type(result) is dict and result.keys()
        # # test repeated results
        # all_results_dups = set([r for r in all_results if
        #                         all_results.count(r) > 1])
        # print(all_results_dups)
        # assert len(list(set(all_results))) == len(all_results)
        # print(all_results)


@pytest.mark.sparql
def test_sparql_printouts_n_result_processing(appglobals, test_wikidetails):
    # test if the prop:value pairs from the test_wikidata_series.rq are
    # still present after the results have been processed and mapped to
    # confIDent
    appglobals()
    aggregated_results = {}
    for i, result in enumerate(iterable=sparql.query(
            source='wikidata',
            class_='Test_Event_Series'), start=1):
        # pprint(result)
        assert len(result['itemLabel']['value']) > 0
        simplified_result = wikidata.sparqlresults_simplify(dataitem=result)
        s_key = simplified_result['item'][0]
        if s_key not in aggregated_results.keys():
            aggregated_results[s_key] = simplified_result
        else:
            aggregated_results[s_key] = sparql.append_nonpresent_vals(
                srcdict=simplified_result, destdict=aggregated_results[s_key])

        for result_title, result_formatted in sparql.process_results(
                results=aggregated_results, source='wikidata',
                out_format='dict', class_='Event_Series'):
            print(result_title, result_formatted, '\n')
            assert result_title
            # sparql has 2 or more non optional props
            assert len(result_formatted) >= 1
            # print(result.items())
            result_vals = [v['value'] for k, v in result.items()]
            print(f'result_vals: {result_vals}')
            result_formatted_val = result_formatted.values()
            print(f'result_formatted_val:{result_formatted_val}')
            result_listofstr = [i for v in result_formatted_val for i in v]
            print(f'result_listofstr: {result_listofstr}')
            samevals = (all(str(i) in result_vals for i in result_listofstr))
            print(samevals)
            # assert samevals is True
            # TODO fix: this test
