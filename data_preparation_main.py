import data_collection
import data_preprocessing
import nltk
import csv
import pandas

##data_collection.extract_movies_and_tv_shows(120000, 121000)
##data_collection.extract_games(0, 1000)
##data_collection.extract_books(1, 1000)

movies = pandas.read_csv('./movies.csv')
movies.set_index('id', inplace=True)
games = pandas.read_csv('./games.csv')
games.set_index('id', inplace=True)
books = pandas.read_csv('./books.csv')
books.set_index('id', inplace=True)

movies_remove_id = []
games_remove_id = []
books_remove_id = []

print(movies.index)

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

print('Preprocessing games name, description and decks...')
for i in range(0, len(games)):
    games.name.values[i] = data_preprocessing.remove_non_alphabet_except_dash(games.name.values[i])
    games.description.values[i] = data_preprocessing.preprocess_text(games.description.values[i])
    games.deck.values[i] = data_preprocessing.preprocess_text(games.deck.values[i])

    if (games.name.values[i] == '' or (games.description.values[i] == '' and games.deck.values[i] == '')):
        games_remove_id.append(games.index[i])


print('Preprocessing books title and description...')
for i in range(0, len(books)):
    books.title.values[i] = data_preprocessing.remove_non_alphabet_except_dash(books.title.values[i])
    books.description.values[i] = data_preprocessing.preprocess_text(books.description.values[i])

    if (books.title.values[i] == '' or books.description.values[i] == ''):
        books_remove_id.append(books.index[i])

print(movies_remove_id)
print(games_remove_id)
print(books_remove_id)

movies.drop(movies_remove_id, inplace=True)
games.drop(games_remove_id, inplace=True)
books.drop(books_remove_id, inplace=True)
    
print('Creating preprocessed_movies.csv...')
movies.to_csv('./preprocessed_movies.csv', sep=',', encoding='utf-8')
print('Creating preprocessed_games.csv...')
games.to_csv('./preprocessed_games.csv', sep=',', encoding='utf-8')
print('Creating preprocessed_books.csv...')
books.to_csv('./preprocessed_books.csv', sep=',', encoding='utf-8')
      
