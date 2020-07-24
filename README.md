# Wikidata Academic Event Series ingestion

**Run:**
* `python -m dataimports`
* wiki template format: `python -m dataimports -f wiki`


**View SPARLQ query**: `dataimports/wikidata/wikidata_series.rq`
which can be copy pasta to [query.wikidata.org](https://query.wikidata.org/)

Result Example (as python dictionary and SPARQL(json) )
```python
{'WikiCFP_conference_series_ID': '37',
 'dateModified': datetime.datetime(2019, 12, 2, 20, 59, 53, tzinfo=datetime.timezone.utc),
 'item': 'http://www.wikidata.org/entity/Q48620041',
 'itemLabel': 'Annual Meeting of the Association for Computational Linguistics',
 'language_usedLabel': 'English',
 'main_subjectLabel': 'natural language processing',
 'short_nameLabel': 'ACL'}
```
```python
{'WikiCFP_conference_series_ID': {'type': 'literal', 'value': '37'},
 'dateModified': {'datatype': 'http://www.w3.org/2001/XMLSchema#dateTime',
                  'type': 'literal',
                  'value': '2019-12-02T20:59:53Z'},
 'item': {'type': 'uri', 'value': 'http://www.wikidata.org/entity/Q48620041'},
 'itemLabel': {'type': 'literal',
               'value': 'Annual Meeting of the Association for Computational '
                        'Linguistics',
               'xml:lang': 'en'},
 'language_usedLabel': {'type': 'literal',
                        'value': 'English',
                        'xml:lang': 'en'},
 'main_subjectLabel': {'type': 'literal',
                       'value': 'natural language processing',
                       'xml:lang': 'en'},
 'short_nameLabel': {'type': 'literal', 'value': 'ACL'}}
```

As Mediawiki template:

```
{{EventSeries
|item=http://www.wikidata.org/entity/Q97594670
|event_interval=1
|event_interval_unitLabel=year
|dateModified=2020-07-22 12:03:45+00:00
|website=https://iiif.io/
|itemLabel=IIIF Conference
|short_nameLabel=IIIF Conference
}}
```

## Requirements
`pip install -r requirements`