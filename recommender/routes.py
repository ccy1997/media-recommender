from flask import render_template, url_for
from recommender import app
from recommender.models import Movie, Game, Book

@app.route("/")
def home():
    return render_template('home.html', title='Media Recommender')