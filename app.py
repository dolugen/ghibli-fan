import requests
from flask import Flask, redirect, render_template
from flask_caching import Cache

API_URL = "https://ghibliapi.herokuapp.com"

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})


def get_url(url, cache_time=60):
    '''caches url content for cache_time duration'''
    @cache.cached(timeout=cache_time, key_prefix=url)
    def get_url_cached(url):
        return requests.get(url)

    return get_url_cached(url)


@app.route('/')
def index():
    return redirect('/movies')


@app.route('/movies')
def movies_list():
    movies_response = get_url(f"{API_URL}/films?limit=250")
    people_response = get_url(f"{API_URL}/people?limit=250")
    all_movies = movies_response.json()
    all_people = people_response.json()

    for movie in all_movies:
        # for this movie, find its people and assign to it
        movie_people = filter(lambda p: movie["url"] in p["films"], all_people)
        movie['people'] = list(movie_people)

    return render_template('movies.html', entries=all_movies)
