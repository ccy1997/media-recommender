from flask import render_template, url_for, request, jsonify
import pandas as pd
import numpy as np
from recommender import app
from recommender import db
from recommender.models import Movie, Game, Book
from recommender.recommender import Recommender, Media

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

@app.route("/submit", methods=['GET'])
def submit():
    favorites_str = request.args.get('favorites')
    favorites = favorites_str.split(',')
    user_favorites_df = create_user_favorites_df(favorites)
    movies_df = movies_table_to_df()
    games_df = games_table_to_df()
    books_df = books_table_to_df()
    r = Recommender(movies_df, games_df, books_df, user_favorites_df)

    # Generate recommendation
    movie_recommendation_df = r.generate_k_recommendations(Media.MOVIE, 2)
    game_recommendation_df = r.generate_k_recommendations(Media.GAME, 2)
    book_recommendation_df = r.generate_k_recommendations(Media.BOOK, 2)

    movie_recommendation_list = []
    game_recommendation_list = []
    book_recommendation_list = []

    for _, row in movie_recommendation_df.iteritems():
        movie_recommendation_list.append(row)

    for _, row in game_recommendation_df.iteritems():
        game_recommendation_list.append(row)

    for _, row in book_recommendation_df.iteritems():
        book_recommendation_list.append(row)
    
    return jsonify({
        'movie': movie_recommendation_list,
        'game': game_recommendation_list,
        'book': book_recommendation_list
    })

def create_user_favorites_df(favorites):
    user_favorites_df = pd.DataFrame(columns=['item_id', 'type'])

    for f in favorites:
        title = f.split('::')[0]
        type = f.split('::')[1]

        if (Media(type) == Media.MOVIE):
            movie = Movie.query.filter(Movie.title.like('%' + title + '%')).first()
            user_favorites_df.loc[len(user_favorites_df)] = [movie.id, type]
        elif (Media(type) == Media.GAME):
            game = Game.query.filter(Game.title.like('%' + title + '%')).first()
            user_favorites_df.loc[len(user_favorites_df)] = [game.id, type]
        elif (Media(type) == Media.BOOK):
            book = Book.query.filter(Book.title.like('%' + title + '%')).first()
            user_favorites_df.loc[len(user_favorites_df)] = [book.id, type]
        else:
            print('Unknown media type: create_users_rating_df')
            return

    return user_favorites_df

def movies_table_to_df():
    movies_df = pd.DataFrame(columns=['id', 'imdb_id', 'title', 'kind', 'votes', 'vector'])

    for movie in Movie.query.all():
        movies_df.loc[len(movies_df)] = [movie.id, movie.imdb_id, movie.title, movie.kind, movie.votes, movie.vector]

    movies_df.set_index('id', inplace=True)
    movies_df['vector'] = [np.fromstring(row['vector'], dtype=float, sep=' ') for i, row in movies_df.iterrows()]

    return movies_df

def games_table_to_df():
    games_df = pd.DataFrame(columns=['id', 'gamespot_id', 'title', 'vector'])

    for game in Game.query.all():
        games_df.loc[len(games_df)] = [game.id, game.gamespot_id, game.title, game.vector]

    games_df.set_index('id', inplace=True)
    games_df['vector'] = [np.fromstring(row['vector'], dtype=float, sep=' ') for i, row in games_df.iterrows()]

    return games_df

def books_table_to_df():
    books_df = pd.DataFrame(columns=['id', 'goodreads_id', 'title', 'isbn', 'isbn13', 'vector'])

    for book in Book.query.all():
        books_df.loc[len(books_df)] = [book.id, book.goodreads_id, book.title, book.isbn, book.isbn13, book.vector]

    books_df.set_index('id', inplace=True)
    books_df['vector'] = [np.fromstring(row['vector'], dtype=float, sep=' ') for i, row in books_df.iterrows()]

    return books_df


    
        