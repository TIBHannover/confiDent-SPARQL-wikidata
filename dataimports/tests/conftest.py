import pytest
import os
from pathlib import Path
from dataimports.file_utils import yaml_get_source, createglobals
from dataimports.mapping import invert_mapping


@pytest.fixture(scope="function")
def find_files():
    def find_files_recursively(filename: str, startdir: str, foundfiles):
        for dir_or_file in os.scandir(startdir):
            if dir_or_file.is_file() and dir_or_file.name == filename:
                foundfiles.append(dir_or_file.path)
            elif dir_or_file.is_dir():
                find_files_recursively(filename=filename,
                                       startdir=dir_or_file.path,
                                       foundfiles=foundfiles)
        return foundfiles
    return find_files_recursively


@pytest.fixture(scope="function")
def test_wikidetails():
    wikidetails = Path(__file__).parent.parent.parent / 'wikidetails.yml'
    if not wikidetails.is_file():
        Path.touch(wikidetails)
    assert wikidetails.is_file()


@pytest.fixture(scope="session")
def appglobals():
    def _createglobals():
        createglobals()
    return _createglobals


@pytest.fixture(scope="session")
def mappings(appglobals):
    appglobals()

    def _getmapping(mapping):
        confid_mapping = yaml_get_source(f'{mapping}/confident_mapping.yml')
        invert_confid_map = invert_mapping(schema=mapping)
        print(f'invert_confid_map: {invert_confid_map}')
        return confid_mapping, invert_confid_map
    return _getmapping


@pytest.fixture(scope="function")
def onevalue():
    def _method():
        return 10
    return _method


@pytest.fixture(scope="function")
def onesparqlresut():
    def _onesparqlresut():
        result = {
            'Twitter_username': {'type': 'literal', 'value': 'swibcon'},
            'dateModified': {
                'datatype': 'http://www.w3.org/2001/XMLSchema#dateTime',
                'type': 'literal', 'value': '2020-07-04T09:34:49Z'},
            'event_interval': {
                'datatype': 'http://www.w3.org/2001/XMLSchema#decimal',
                'type': 'literal', 'value': '1'},
            'event_interval_unitLabel': {'type': 'literal', 'value': 'year'},
            'item': {'type': 'uri',
                     'value': 'http://www.wikidata.org/entity/Q29129469'},
            'itemLabel': {'type': 'literal',
                          'value': 'Semantic Web in Libraries Conference',
                          'xml:lang': 'en'},
            'locationLabel': {'type': 'literal', 'value': 'Hamburg',
                              'xml:lang': 'en'},
            'official_website': {'type': 'uri', 'value': 'http://swib.org'},
            'short_nameLabel': {'type': 'literal', 'value': 'SWIB'},
            'NonMatchingKey': {'type': 'literal', 'value': 'FOO'}}
        return result
    return _onesparqlresut


@pytest.fixture(scope="function")
def one_dataitem_confikeys():
    def one_dataitem():
        result = {
            'Twitter': {'type': 'literal', 'value': 'swibcon'},
            'Event Frequency': {
                'datatype': 'http://www.w3.org/2001/XMLSchema#decimal',
                'type': 'literal', 'value': '1'},
            'WDQID': {'type': 'uri',
                      'value': 'http://www.wikidata.org/entity/Q29129469'},
            'official_name': {'type': 'literal',
                              'value': 'Semantic Web in Libraries Conference',
                              'xml:lang': 'en'},
            'Website': {'type': 'uri', 'value': 'http://swib.org'},
            'acronym': {'type': 'literal', 'value': 'SWIB'}}
        return result
    return one_dataitem
