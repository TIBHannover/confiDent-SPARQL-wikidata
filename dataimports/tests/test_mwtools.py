import pytest
import string
from random import choice
from time import sleep
from mediawikitools.__init__ import site
from mediawikitools.wiki import actions


def randstring(lenght=10):
    out = "".join([choice(list(string.ascii_letters)) for n in range(lenght)])
    return out


def test_site():
    major, minor, patch = site.version
    assert major == 1 and minor > 30


def test_user():
    assert len(site.username) > 0


@pytest.mark.mw_ask
def test_ask():
    # should only happen if SMW is installed. Use API find that
    response = actions.ask(query='[[Category:Event]]|?Event Type')
    print(response)
    assert len(response) > 0


@pytest.mark.mw_ask
def test_ask_nonexistant_prop():
    randomprop = randstring(5)
    q = f'[[{randomprop}::+]]'
    response = actions.ask(query=q)
    print(q, response)
    assert response == []


@pytest.mark.mw_write
def test_write_and_ask():
    randomval = randstring(10).capitalize()  # mw capitalizes val
    prop = f'[[TestProp::{randomval}]]'
    print('property:', prop)
    actions.edit(page='Test', content=prop, summary='Testing property writing',
                 append=True)
    response = actions.ask(query=f'{prop}|?TestProp')
    print(prop, response)
    assert response[0]['page'] == 'Test'
    assert response[0]['TestProp'] == randomval


@pytest.mark.mw_write
def test_edit():
    rstring = randstring(10)
    pagename = 'Test'
    actions.edit(page=pagename, content=f'Edit {rstring} by ~~~~',
                 summary='Testing overwriting', append=False)
    content, lastedit = actions.read(page=pagename)
    assert rstring in content

    # Test append=True
    appendrstring = randstring(10)
    actions.edit(page=pagename, content=f'Edit {appendrstring} by ~~~~',
                 summary='Testing appending', append=True)
    content, lastedit = actions.read(page=pagename)
    assert appendrstring in content

    # Test write to existing page with newpageonly=True
    # nothing should be written
    newrstring = randstring(10)
    actions.edit(page=pagename, content=f'Edit {newrstring} by ~~~~',
                 newpageonly=True)
    assert newrstring not in content


@pytest.mark.mw_write
def test_edit_samecontent():
    # Test should succeed if the same content is not written to the page
    # since it is well ... the same
    pagename = 'Test'
    test_content = "Hello \n'''wiki page'''"
    new_content = "This is new content"
    actions.edit(page=pagename, content=test_content,
                 summary='Testing writing', append=False)
    wiki_page_content = (actions.read(page=pagename))[0]

    if wiki_page_content != test_content:
        actions.edit(page=pagename, content=new_content,
                     summary='Testing writing',
                     append=False)
    actual_content = (actions.read(page=pagename))[0]
    assert actual_content != new_content
    assert actual_content == test_content


@pytest.mark.mw_write
def test_edit_protected_page():
    edit_result = actions.edit(page='PIDapalooza', content='Edit by ~~~~',
                               summary='Testing writing', append=True)
    assert edit_result is False
    edit_result = actions.edit(page='Test', content='Edit by ~~~~',
                               summary='Testing writing', append=True)
    assert edit_result is True


@pytest.mark.skip(reason="test takes to long")
def test_largenumber_edits():
    # test if mw api rate limit is not exceeded
    for i in range(500):
        rstring = randstring(10)
        print(i, rstring)
        pagename = 'Test'
        sleep(1)
        actions.edit(page=pagename, content=f'Edit {rstring} by ~~~~',
                     summary='Testing overwriting', append=False)
