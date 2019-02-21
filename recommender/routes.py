from flask import render_template, url_for, request, jsonify
from recommender import app
from recommender import db
from recommender.models import Movie, Game, Book

@app.route("/")
def home():
    return render_template('home.html', title='Media Recommender')

@app.route("/search", methods=['GET'])
def search():
    query = request.args.get('query')
    movie_results = Movie.query.filter(Movie.title.like('%' + query + '%')).all()
    game_results = Game.query.filter(Game.title.like('%' + query + '%')).all()
    book_results = Book.query.filter(Book.title.like('%' + query + '%')).all()
    results = movie_results + game_results + book_results
    titles = [r.title + '::' + type(r).__name__ for r in results][0:10]
    return jsonify({'results': titles})
        