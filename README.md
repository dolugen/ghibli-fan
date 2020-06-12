# Ghibli Movies

A single page website that lists all of Ghibli movies.

## Running Locally

Make sure you have Python 3.7 [installed locally](http://install.python-guide.org). To push to Heroku, you'll need to install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).

```sh
$ git clone https://github.com/dolugen/ghibli-fan.git
$ cd ghibli-fan

$ python3 -m venv env
$ source ./env/bin/activate
$ pip install -r requirements.txt

$ heroku local
```

Your app should now be running on [localhost:5000](http://localhost:5000/).

## Testing

```
$ pytest tests.py
```

## Deploying to Heroku

```sh
$ heroku create
$ git push heroku master

$ heroku open
```
or

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

## Documentation

For more information about using Python on Heroku, see these Dev Center articles:

- [Python on Heroku](https://devcenter.heroku.com/categories/python)
