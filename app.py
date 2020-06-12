import requests
from flask import Flask, redirect, render_template
from flask_caching import Cache

API_URL = "https://ghibliapi.herokuapp.com"

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

class GhibliException(Exception):
    '''generic exception for app error handling'''
    pass


def get_url(url, cache_time=60):
    '''caches url content for cache_time duration'''
    @cache.cached(timeout=cache_time, key_prefix=url)
    def get_url_cached(url):
        return requests.get(url)

    return get_url_cached(url)

def get_ghibli_api_resource(name, limit=250):
    '''load a resource from the ghibli api'''
    response = get_url(f"{API_URL}/{name}?limit={limit}")
    if response.status_code != 200:
        raise Exception(f'Resource unavailable! Response code: {response.status_code}')

    return response.json()


def get_movies_list():
    return get_ghibli_api_resource('films')


def get_people_list():
    return get_ghibli_api_resource('people')


def get_movies_and_people():
    movies = get_movies_list()
    people = get_people_list()

    for movie in movies:
        # for this movie, find its people and assign to it
        movie_people = filter(lambda p: movie["url"] in p["films"], people)
        movie['people'] = list(movie_people)
    
    return movies


@app.route('/')
def index():
    return redirect('/movies')


@app.route('/movies')
def movies_list():
    api_error = False
    try:
        movies = get_movies_and_people()
    except:
        movies = []
        api_error = True
    return render_template('movies.html', entries=movies, api_error=api_error)
