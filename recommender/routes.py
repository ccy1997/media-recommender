from recommender import app
from recommender.models import Movie, Game, Book

@app.route("/")
def home():
    return "home"