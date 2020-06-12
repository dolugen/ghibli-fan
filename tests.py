from unittest.mock import Mock
import json
import logging
import requests
import pytest
from pytest_mock import mocker
from requests import Response


from app import app,  get_movies_and_people, get_movies_list, get_people_list, get_ghibli_api_resource

@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()


@pytest.fixture
def movies_json():
    with open('test_data/movies.json') as f:
        yield json.loads(f.read())


@pytest.fixture
def people_json():
    with open('test_data/people.json') as f:
        yield json.loads(f.read())


def test_movies_page(client, mocker):
    '''
    test that movies page is available and
    uses get_movies_and_people function
    '''
    get_movies_and_people = mocker.patch('app.get_movies_and_people')
    r = client.get('/movies')
    assert r.status_code == 200
    get_movies_and_people.assert_called()


def test_get_movies_list(mocker):
    '''test that a correct request is sent for movies'''
    get_ghibli_api_resource = mocker.patch('app.get_ghibli_api_resource')
    get_ghibli_api_resource.status_code.return_value = 200
    get_movies_list()
    get_ghibli_api_resource.assert_called_with('films')

def test_get_people_list(mocker):
    '''test that a correct request is sent for people'''
    get_ghibli_api_resource = mocker.patch('app.get_ghibli_api_resource')
    get_ghibli_api_resource.status_code = 200
    get_people_list()
    get_ghibli_api_resource.assert_called_with('people')

def test_api_call_for_films(mocker):
    '''test that api calls are correct'''
    get_url = mocker.patch('app.get_url')
    res = Mock(Response)
    res.status_code = 200
    res.json.return_value = []
    get_url.return_value = res
    get_ghibli_api_resource('films')
    get_url.assert_called_with("https://ghibliapi.herokuapp.com/films?limit=250")

    get_ghibli_api_resource('people')
    get_url.assert_called_with("https://ghibliapi.herokuapp.com/people?limit=250")


def test_get_movies_and_people(mocker, movies_json, people_json):
    '''test that movies are correctly annotated with people'''
    get_movies_list = mocker.patch('app.get_movies_list')
    get_people_list = mocker.patch('app.get_people_list')
    get_movies_list.return_value = movies_json
    get_people_list.return_value = people_json

    movies_with_people = get_movies_and_people()
    get_movies_list.assert_called_once()
    get_people_list.assert_called_once()
    
    # the first movie in the dataset
    movie = movies_with_people[0]
    assert movie['title'] == 'Castle in the Sky'
    # the only person for this movie
    person = movie['people'][0]
    assert person['name'] == 'Colonel Muska'
    assert person['films'] == [movie['url']]