from gensim.utils import simple_preprocess
from gensim.test.utils import get_tmpfile
from gensim.models import Word2Vec
import csv
import sys
from os import listdir
from parameters import Parameters
from data_preprocessing import lemmatize_words
from data_preprocessing import remove_html_tags
from data_preprocessing import preprocess_text_for_word2vec


def prepare_word2vec_training_data():
    processed_movie_documents = read_movie_documents()
    processed_game_documents = read_game_documents()
    processed_book_documents = read_book_documents()
    return processed_movie_documents + processed_game_documents + processed_book_documents


def read_movie_documents():
    print('Processing movie documents...')
    csv.field_size_limit(300000)
    processed_movie_documents = []
    with open(f'{Parameters.word2vec_train_data_path}movies_metadata.csv', encoding="utf-8") as movie_metadata_csv:
        csv_reader = csv.reader(movie_metadata_csv, delimiter=',')
        for i, row in enumerate(csv_reader):
            print(f'iter = {i}, file = movies_metadata.csv')
            if i != 0:
                raw_document = row[9]
                processed_document = preprocess_text_for_word2vec(raw_document)
                processed_movie_documents.append(processed_document)
    with open(f'{Parameters.generated_data_path}{Parameters.raw_movie_csv_name}', encoding="utf-8") as generated_movie_csv:
        csv_reader = csv.reader(generated_movie_csv, delimiter=',')
        for i, row in enumerate(csv_reader):
            print(f'iter = {i}, file = raw_movies.csv')
            if i != 0:
                raw_documents = row[5].split('::')
                processed_documents = [preprocess_text_for_word2vec(d) for d in raw_documents]
                processed_movie_documents += processed_documents
    return processed_movie_documents


def read_game_documents():
    print('Processing game documents...')
    csv.field_size_limit(300000)
    processed_game_documents = []
    with open(f'{Parameters.word2vec_train_data_path}games_features.csv', encoding="utf-8") as game_features_csv:
        csv_reader = csv.reader(game_features_csv, delimiter=',')
        for i, row in enumerate(csv_reader):
            print(f'iter = {i}, file = games_features.csv')
            if i != 0:
                raw_document = row[61]
                processed_document = preprocess_text_for_word2vec(raw_document)
                processed_game_documents.append(processed_document)
    with open(f'{Parameters.generated_data_path}{Parameters.raw_game_csv_name}', encoding="utf-8") as generated_game_csv:
        csv_reader = csv.reader(generated_game_csv, delimiter=',')
        for i, row in enumerate(csv_reader):
            print(f'iter = {i}, file = raw_games.csv')
            if i != 0:
                raw_documents = row[4].split('::')
                processed_documents = [preprocess_text_for_word2vec(d) for d in raw_documents]
                processed_game_documents += processed_documents
    return processed_game_documents


def read_book_documents():
    print('Reading book documents...')
    csv.field_size_limit(300000)
    processed_book_documents = []
    with open(f'{Parameters.word2vec_train_data_path}booksummaries.txt', encoding='utf-8') as book_summaries_csv:
        csv_reader = csv.reader(book_summaries_csv, delimiter='\t')
        for i, row in enumerate(csv_reader):
            print(f'iter = {i}, file = booksummaries.txt')
            if i != 0:
                raw_document = row[6]
                processed_document = preprocess_text_for_word2vec(raw_document)
                processed_book_documents.append(processed_document)
    with open(f'{Parameters.generated_data_path}{Parameters.raw_book_csv_name}', encoding="utf-8") as generated_book_csv:
        csv_reader = csv.reader(generated_book_csv, delimiter=',')
        for i, row in enumerate(csv_reader):
            print(f'iter = {i}, file = raw_books.csv')
            if i != 0:
                raw_documents = row[4].split('::')
                processed_documents = [preprocess_text_for_word2vec(d) for d in raw_documents]
                processed_book_documents += processed_documents
    return processed_book_documents


def word2vec_train(training_documents):
    print(len(training_documents))
    print('Training model...')
    model = Word2Vec(training_documents, size=50, min_count=2, workers=4)
    model.train(training_documents, total_examples=len(training_documents), epochs=10)
    print('Model trained')
    return model


def save_model_vectors(model):
    word_vectors = model.wv
    word_vectors.save(f'{Parameters.generated_data_path}word_vectors.kv')


def main():
    training_documents = prepare_word2vec_training_data()
    model = word2vec_train(training_documents)
    save_model_vectors(model)


if __name__ == '__main__':
    main()
    