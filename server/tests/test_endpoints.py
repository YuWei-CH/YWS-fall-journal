from http.client import (
    BAD_REQUEST,
    FORBIDDEN,
    NOT_ACCEPTABLE,
    NOT_FOUND,
    OK,
    SERVICE_UNAVAILABLE,
)

from unittest.mock import patch

import pytest, json

from data.people import NAME, AFFILIATION, EMAIL, ROLES

import server.endpoints as ep

TEST_CLIENT = ep.app.test_client()

import data.text as txt
import data.roles as rls
from data.text import *
import data.manuscript as ms

TEST_EMAIL = "testEmail@gmail.com"
TEST_TITLE = "Test Manuscript Title"
TEST_PAGE_NUMBER = "TestPageNumber"


def test_hello():
    resp = TEST_CLIENT.get(ep.HELLO_EP)
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert ep.HELLO_RESP in resp_json


def test_title():
    resp = TEST_CLIENT.get(ep.TITLE_EP)
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert ep.TITLE_RESP in resp_json
    assert isinstance(resp_json[ep.TITLE_RESP], str)
    assert len(resp_json[ep.TITLE_RESP]) > 0


@patch('data.people.read', autospec=True,
        return_value={'id': {NAME: 'Joe Schmoe'}})
def test_read_people(mock_read):
    resp = TEST_CLIENT.get(ep.PEOPLE_EP)
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    for _id, person in resp_json.items():
        assert isinstance(_id, str)
        assert len(_id) > 0
        assert NAME in person


@patch('data.people.read_one', autospec=True,
       return_value={NAME: 'Joe Schmoe'})
def test_read_one_person(mock_read):
    resp = TEST_CLIENT.get(f'{ep.PEOPLE_EP}/mock_id')
    assert resp.status_code == OK


@patch('data.people.read_one', autospec=True, return_value=None)
def test_read_one_person_not_found(mock_read):
    resp = TEST_CLIENT.get(f'{ep.PEOPLE_EP}/mock_id')
    assert resp.status_code == NOT_FOUND


@patch('data.people.delete', autospec=True, return_value=TEST_EMAIL)
def test_delete_people(mock_delete):
    resp = TEST_CLIENT.delete(f'{ep.PEOPLE_EP}/mock_email')
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert ep.DELETED in resp_json


@patch('data.people.delete', autospec=True, return_value=None)
def test_delete_people_not_found(mock_delete):
    resp = TEST_CLIENT.delete(f'{ep.PEOPLE_EP}/mock_email')
    assert resp.status_code == NOT_FOUND


CREATE_TEST_DATA = {
    NAME: "Test Name",
    AFFILIATION: "Test Affiliation",
    EMAIL: TEST_EMAIL,
    ROLES: rls.TEST_CODE
}


@patch('data.people.create', autospec=True, return_value=TEST_EMAIL)
def test_create_people(mock_create):
    resp = TEST_CLIENT.put(
        f'{ep.PEOPLE_EP}/create',
        data=json.dumps(CREATE_TEST_DATA),
        content_type='application/json'
    )
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert ep.MESSAGE in resp_json
    assert ep.RETURN in resp_json


@patch('data.people.create', autospec=True, side_effect=ValueError("Mocked Exception"))
def test_create_people_failed(mock_create):
    resp = TEST_CLIENT.put(
        f'{ep.PEOPLE_EP}/create',
        data=json.dumps(CREATE_TEST_DATA),
        content_type='application/json'
    )
    assert resp.status_code == NOT_ACCEPTABLE


UPDATE_PEOPLE_DATA = {
    EMAIL: TEST_EMAIL,
    NAME: "Yirong Wang",
    AFFILIATION: "NYU",
}


@patch('data.people.update', autospec=True, return_value=TEST_EMAIL)
def test_update_people(mock_update):
    resp = TEST_CLIENT.put(
        f'{ep.PEOPLE_EP}/update',
        data=json.dumps(UPDATE_PEOPLE_DATA),
        content_type='application/json'
    )
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert ep.MESSAGE in resp_json
    assert ep.RETURN in resp_json


@patch('data.people.update', autospec=True, side_effect=ValueError("Mocked Exception"))
def test_update_people_failed(mock_update):
    resp = TEST_CLIENT.put(
        f'{ep.PEOPLE_EP}/update',
        data=json.dumps(UPDATE_PEOPLE_DATA),
        content_type='application/json'
    )
    assert resp.status_code == NOT_ACCEPTABLE


ADD_DELETE_ROLE_DATA = {
    EMAIL: TEST_EMAIL,
    ep.ROLE: rls.TEST_CODE
}


@patch('data.people.add_role', autospec=True, return_value=TEST_EMAIL)
def test_add_role(mock_add_role):
    resp = TEST_CLIENT.put(
        f'{ep.PEOPLE_EP}/add_role',
        data=json.dumps(ADD_DELETE_ROLE_DATA),
        content_type='application/json'
    )
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert ep.MESSAGE in resp_json
    assert ep.RETURN in resp_json


@patch('data.people.add_role', autospec=True, side_effect=ValueError("Mocked Exception"))
def test_add_role_failed(mock_add_role):
    resp = TEST_CLIENT.put(
        f'{ep.PEOPLE_EP}/add_role',
        data=json.dumps(ADD_DELETE_ROLE_DATA),
        content_type='application/json'
    )
    assert resp.status_code == NOT_ACCEPTABLE


@patch('data.people.delete_role', autospec=True, return_value=TEST_EMAIL)
def test_delete_role(mock_delete_role):
    resp = TEST_CLIENT.delete(
        f'{ep.PEOPLE_EP}/delete_role',
        data=json.dumps(ADD_DELETE_ROLE_DATA),
        content_type='application/json'
    )
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert ep.MESSAGE in resp_json
    assert ep.RETURN in resp_json


@patch('data.people.delete_role', autospec=True, side_effect=ValueError("Mocked Exception"))
def test_delete_role_failed(mock_delete_role):
    resp = TEST_CLIENT.delete(
        f'{ep.PEOPLE_EP}/delete_role',
        data=json.dumps(ADD_DELETE_ROLE_DATA),
        content_type='application/json'
    )
    assert resp.status_code == NOT_ACCEPTABLE


@patch('data.text.read', autospec=True,
       return_value={'page_number': {TITLE: 'Test Title', TEXT: 'Test Text'}})
def test_read_text(mock_read):
    resp = TEST_CLIENT.get(ep.TEXT_EP)
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    for page_number, text in resp_json.items():
        assert isinstance(page_number, str)
        assert len(page_number) > 0
        assert TITLE in text
        assert TEXT in text


@patch('data.text.read_one', autospec=True,
       return_value={TITLE: 'Test Title', TEXT: 'Test Text'})
def test_read_one_text(mock_read):
    resp = TEST_CLIENT.get(f'{ep.TEXT_EP}/mock_page_number')
    assert resp.status_code == OK


@patch('data.text.read_one', autospec=True, return_value=None)
def test_read_one_text_not_found(mock_read):
    resp = TEST_CLIENT.get(f'{ep.TEXT_EP}/mock_page_number')
    assert resp.status_code == NOT_FOUND


TEXT_CREATE_TEST_DATA = {
    TITLE: "Test Title",
    TEXT: "Test Text",
    PAGE_NUMBER: TEST_PAGE_NUMBER,
}


@patch('data.text.create', autospec=True, return_value=TEST_PAGE_NUMBER)
def test_create_text(mock_create):
    resp = TEST_CLIENT.put(
        f'{ep.TEXT_EP}/create',
        data=json.dumps(TEXT_CREATE_TEST_DATA),
        content_type='application/json'
    )
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert ep.MESSAGE in resp_json
    assert ep.RETURN in resp_json


@patch('data.text.create', autospec=True, side_effect=ValueError("Mocked Exception"))
def test_create_text_failed(mock_create):
    resp = TEST_CLIENT.put(
        f'{ep.TEXT_EP}/create',
        data=json.dumps(TEXT_CREATE_TEST_DATA),
        content_type='application/json'
    )
    assert resp.status_code == NOT_ACCEPTABLE


@patch('data.text.delete', autospec=True, return_value=TEST_PAGE_NUMBER)
def test_delete_text(mock_delete):
    resp = TEST_CLIENT.delete(f'{ep.TEXT_EP}/mock_page_number')
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert ep.DELETED in resp_json


@patch('data.text.delete', autospec=True, return_value=None)
def test_delete_text_not_found(mock_delete):
    resp = TEST_CLIENT.delete(f'{ep.TEXT_EP}/mock_page_number')
    assert resp.status_code == NOT_FOUND


UPDATE_TEXT_DATA = {
    txt.PAGE_NUMBER: TEST_PAGE_NUMBER,
    ep.FIELD: txt.TITLE, 
    ep.VALUE: "Test Title",
}


@patch('data.text.update', autospec=True, return_value=TEST_PAGE_NUMBER)
def test_update_text(mock_update):
    resp = TEST_CLIENT.put(
        f'{ep.TEXT_EP}/update',
        data=json.dumps(UPDATE_TEXT_DATA),
        content_type='application/json'
    )
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert ep.MESSAGE in resp_json
    assert ep.RETURN in resp_json


@patch('data.text.update', autospec=True, side_effect=ValueError("Mocked Exception"))
def test_update_text_failed(mock_update):
    resp = TEST_CLIENT.put(
        f'{ep.TEXT_EP}/update',
        data=json.dumps(UPDATE_TEXT_DATA),
        content_type='application/json'
    )
    assert resp.status_code == NOT_ACCEPTABLE


@patch('data.people.get_masthead', autospec=True, return_value={})
def test_get_masthead(mock_get_masthead):
    resp = TEST_CLIENT.get(f'{ep.PEOPLE_EP}/masthead')
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert ep.MASTHEAD in resp_json


MANUSCRIPT_DATA = {
    ms.TITLE: "Test Manuscript",
    ms.AUTHOR: "Test Author",
    ms.AUTHOR_EMAIL: TEST_EMAIL, 
    ms.TEXT: "Test Text", 
    ms.ABSTRACT: "Test Abstract", 
    ms.EDITOR_EMAIL: TEST_EMAIL
}


@patch('data.manuscript.read', autospec=True,
       return_value={'title': {ms.TITLE: 'Test Title'}})
def test_read_manuscripts(mock_read):
    resp = TEST_CLIENT.get(ep.MANUSCRIPT_EP)
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    for title, manu in resp_json.items():
        assert isinstance(title, str)
        assert len(title) > 0
        assert ms.TITLE in manu


@patch('data.manuscript.read_one', autospec=True,
       return_value={ms.TITLE: 'Test Title'})
def test_read_one_manuscript(mock_read):
    resp = TEST_CLIENT.get(f'{ep.MANUSCRIPT_EP}/mock_title')
    assert resp.status_code == OK


@patch('data.manuscript.read_one', autospec=True, return_value=None)
def test_read_one_manuscript_not_found(mock_read):
    resp = TEST_CLIENT.get(f'{ep.MANUSCRIPT_EP}/mock_title')
    assert resp.status_code == NOT_FOUND


@patch('data.manuscript.delete', autospec=True, return_value=TEST_TITLE)
def test_delete_manuscript(mock_delete):
    resp = TEST_CLIENT.delete(f'{ep.MANUSCRIPT_EP}/mock_title')
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert ep.DELETED in resp_json


@patch('data.manuscript.delete', autospec=True, return_value=None)
def test_delete_manuscript_not_found(mock_delete):
    resp = TEST_CLIENT.delete(f'{ep.MANUSCRIPT_EP}/mock_title')
    assert resp.status_code == NOT_FOUND


@patch('data.manuscript.create', autospec=True, return_value=TEST_TITLE)
def test_create_manuscript(mock_create):
    resp = TEST_CLIENT.put(
        f'{ep.MANUSCRIPT_EP}/create',
        data=json.dumps(MANUSCRIPT_DATA),
        content_type='application/json'
    )
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert ep.MESSAGE in resp_json
    assert ep.RETURN in resp_json


@patch('data.manuscript.create', autospec=True, side_effect=ValueError("Mocked Exception"))
def test_create_manuscript_failed(mock_create):
    resp = TEST_CLIENT.put(
        f'{ep.MANUSCRIPT_EP}/create',
        data=json.dumps(MANUSCRIPT_DATA),
        content_type='application/json'
    )
    assert resp.status_code == NOT_ACCEPTABLE


@patch('data.manuscript.update', autospec=True, return_value=TEST_TITLE)
def test_update_manuscript(mock_update):
    resp = TEST_CLIENT.put(
        f'{ep.MANUSCRIPT_EP}/update',
        data=json.dumps(MANUSCRIPT_DATA),
        content_type='application/json'
    )
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert ep.MESSAGE in resp_json
    assert ep.RETURN in resp_json


@patch('data.manuscript.update', autospec=True, side_effect=ValueError("Mocked Exception"))
def test_update_manuscript_failed(mock_update):
    resp = TEST_CLIENT.put(
        f'{ep.MANUSCRIPT_EP}/update',
        data=json.dumps(MANUSCRIPT_DATA),
        content_type='application/json'
    )
    assert resp.status_code == NOT_ACCEPTABLE
