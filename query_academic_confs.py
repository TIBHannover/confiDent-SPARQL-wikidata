from SPARQLWrapper import SPARQLWrapper, TURTLE, JSON, RDF
from pprint import pprint


endpoint = SPARQLWrapper("https://query.wikidata.org/sparql")
with open("wikidata_academic_conferences.rq", "r") as sparql_f:
    sparql = sparql_f.read()

endpoint.setQuery(sparql)
endpoint.setReturnFormat(JSON)
results = endpoint.query().convert()

results_bindings = results['results']['bindings']

for entry in results_bindings :
    pprint(entry)
    print('\n')

print('Results returned:', len(results['results']['bindings']))
print(len(results_bindings))