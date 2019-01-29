import data_collection
import data_preprocessing
import feature_extractor
import nltk
import csv
import pandas
import gensim
import recommender
import numpy as np

# Data collection from various sources, stored in csv file
##data_collection.extract_movies_and_tv_shows(120000, 121000)
##data_collection.extract_games(0, 1000)
##data_collection.extract_books(1, 1000)

# Load the csv files
movies = pandas.read_csv('./movies.csv')
movies.set_index('id', inplace=True)
games = pandas.read_csv('./games.csv')
games.set_index('id', inplace=True)
books = pandas.read_csv('./books.csv')
books.set_index('id', inplace=True)

# Lists for storing ids of the items to be removed
movies_remove_id = []
games_remove_id = []
books_remove_id = []

# Preprocess movies data
print('Preprocessing movies title, synopses and summaries...')
for i in range(0, len(movies)):
    movies.title.values[i] = data_preprocessing.remove_non_alphabet_except_dash(movies.title.values[i])
    movies.synopsis.values[i] = data_preprocessing.preprocess_text(movies.synopsis.values[i])
    movie_summaries = movies.summaries.values[i].split('::')

    for j in range(0, len(movie_summaries)):
        movie_summaries[j] = data_preprocessing.preprocess_text(movie_summaries[j])

    movies.summaries.values[i] = '::'.join(movie_summaries)

    if (movies.title.values[i] == '' or (movies.synopsis.values[i] == '' and movies.summaries.values[i] == '')):
        movies_remove_id.append(movies.index[i])

# Preprocess games data
print('Preprocessing games name, description and decks...')
for i in range(0, len(games)):
    games.name.values[i] = data_preprocessing.remove_non_alphabet_except_dash(games.name.values[i])
    games.description.values[i] = data_preprocessing.preprocess_text(games.description.values[i])
    games.deck.values[i] = data_preprocessing.preprocess_text(games.deck.values[i])

    if (games.name.values[i] == '' or (games.description.values[i] == '' and games.deck.values[i] == '')):
        games_remove_id.append(games.index[i])

# Preprocess books data
print('Preprocessing books title and description...')
for i in range(0, len(books)):
    books.title.values[i] = data_preprocessing.remove_non_alphabet_except_dash(books.title.values[i])
    books.description.values[i] = data_preprocessing.preprocess_text(books.description.values[i])

    if (books.title.values[i] == '' or books.description.values[i] == ''):
        books_remove_id.append(books.index[i])

# Drop all items with empty title or description
movies.drop(movies_remove_id, inplace=True)
games.drop(games_remove_id, inplace=True)
books.drop(books_remove_id, inplace=True)

# Load pre-trained model based on google news dataset
print('Loading model...')
item_vector_model = gensim.models.KeyedVectors.load_word2vec_format( './GoogleNews-vectors-negative300.bin', binary=True)

# Lists for storing item vectors
movie_vectors = []
game_vectors = []
book_vectors = []

# Calculating movie vectors
for i, row in movies.iterrows():
    print('Calculating movie_vector: id = ' + str(i))
    movie_vectors.append(feature_extractor.calculate_item_vector(row['synopsis'].split(' ') + row['summaries'].replace('::', ' ').split(' '), item_vector_model.vector_size, item_vector_model))

# Calculating game vectors
for i, row in games.iterrows():
    print('Calculating game_vector: id = ' + str(i))
    game_vectors.append(feature_extractor.calculate_item_vector(row['description'].split(' ') + row['deck'].split(' '), item_vector_model.vector_size, item_vector_model))

# Calculating book vectors
for i, row in books.iterrows():
    print('Calculating book_vector: id = ' + str(i))
    book_vectors.append(feature_extractor.calculate_item_vector(row['description'].split(' '), item_vector_model.vector_size, item_vector_model))

item_type = input('Enter the type of item you want to choose (movie, game or book):\n')
i = int(input('Enter the ID of the item you like:\n'))

if item_type == 'movie':
    pos = movies.index.get_loc(i)
    user_vector = movie_vectors[pos]
    recommender.generate_k_recommendations(user_vector.reshape(1, item_vector_model.vector_size), np.array(movie_vectors), movies, 3)
elif item_type == 'game':
    pos = games.index.get_loc(i)
    user_vector = game_vectors[pos]
    recommender.generate_k_recommendations(user_vector.reshape(1, item_vector_model.vector_size), np.array(game_vectors), games, 3)
elif item_type == 'book':
    pos = books.index.get_loc(i)
    user_vector = book_vectors[pos]
    recommender.generate_k_recommendations(user_vector.reshape(1, item_vector_model.vector_size), np.array(book_vectors), books, 3)

# Store the preprocessed data into csv files
##print('Creating preprocessed_movies.csv...')
##movies.to_csv('./preprocessed_movies.csv', sep=',', encoding='utf-8')
##print('Creating preprocessed_games.csv...')
##games.to_csv('./preprocessed_games.csv', sep=',', encoding='utf-8')
##print('Creating preprocessed_books.csv...')
##books.to_csv('./preprocessed_books.csv', sep=',', encoding='utf-8')
    
