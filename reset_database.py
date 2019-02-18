# A script for resetting server's database

from recommender import db
from recommender.models import Movie, Game, Book
import pandas as pd

# Clear the database first
db.drop_all()

# Create tables for all models
db.create_all()

# Read items in DataFrame
movie_df = pd.read_csv('./vectorized_movies.csv')
movie_df.set_index('id', inplace=True)
game_df = pd.read_csv('./vectorized_games.csv')
game_df.set_index('id', inplace=True)
book_df = pd.read_csv('./vectorized_books.csv')
book_df.set_index('id', inplace=True)

# Populate movie table
for i, row in movie_df.iterrows():
    movie = Movie(
        id=i, 
        imdb_id=row['imdb_id'], 
        title=row['title'], 
        kind=row['kind'], 
        votes=row['votes'], 
        vector=row['vector']
        )
    db.session.add(movie)

db.session.commit()

# Populate game table
for i, row in game_df.iterrows():
    game = Game(
        id=i, 
        gamespot_id=row['gamespot_id'], 
        title=row['title'], 
        vector=row['vector']
        )
    db.session.add(game)

db.session.commit()

# Populate book table
for i, row in book_df.iterrows():
    book = Book(
        id=i, 
        goodreads_id=row['goodreads_id'], 
        title=row['title'], 
        isbn=row['isbn'],
        isbn13=row['isbn13'], 
        vector=row['vector']
        )
    db.session.add(book)

db.session.commit()

# Test stuff
# print(Movie.query.all())
# print(Game.query.all())
# print(Book.query.first())