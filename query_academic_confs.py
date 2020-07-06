from SPARQLWrapper import SPARQLWrapper, TURTLE, JSON, RDF

sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
sparql.setQuery("""
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX wikibase: <http://wikiba.se/ontology#>
    PREFIX bd: <http://www.bigdata.com/rdf#>
    
    SELECT ?item ?itemLabel
    WHERE
    {
        # wdt:P31 (instance of)  wd:Q47258130 (academic conferences)
        ?item wdt:P31 wd:Q47258130 .
        ?item rdfs:label ?label .  
            FILTER (LANG(?label) = "en") . 			
            BIND (str(?label) AS ?itemLabel) .
        }
    LIMIT 5
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for entry in results['results']['bindings']:
    print(entry)

