import data_collection
import data_preprocessing
import nltk
import csv
import pandas

##data_collection.extract_movies_and_tv_shows(120000, 121000)
##data_collection.extract_games(0, 1000)
##data_collection.extract_books(1, 1000)

movies = pandas.read_csv('./movies.csv')
games = pandas.read_csv('./games.csv')
books = pandas.read_csv('./books.csv')

movies_synopses = movies.synopsis.values
movies_summaries = movies.summaries.values
games_descs = games.description.values
games_decks = games.deck.values
books_descs = books.description.values

for i in range(0, len(movies_synopses)):
    movies_synopses[i] = data_preprocessing.preprocess_text(movie_synopses[i])

for i in range(0, len(movies_summaries)):
    movie_summaries = movies_summaries[i].split('::')

    for j in range(0, len(movie_summaries)):
        movie_summaries[i] = data_preprocessing.preprocess_text(movie_summaries[i])

    movies_summaries[i] = '::'.join(movie_summaries)

for i in range(0, len(games_descs)):
    games_descs[i] = data_preprocessing.preprocess_text(game_descs[i])

for i in range(0, len(games_decks)):
    games_decks[i] = data_preprocessing.preprocess_text(game_decks[i])

for i in range(0, len(books_descs)):
    books_descs[i] = data_preprocessing.preprocess_text(book_descs[i])

movies.to_csv('./preprocessed_movies.csv', sep=',', encoding='utf-8')
games.to_csv('./preprocessed_games.csv', sep=',', encoding='utf-8')
books.to_csv('./preprocessed_books.csv', sep=',', encoding='utf-8')

    



