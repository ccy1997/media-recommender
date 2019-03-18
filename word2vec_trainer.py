from gensim.utils import simple_preprocess
from gensim.test.utils import get_tmpfile
from gensim.models import Word2Vec
import csv
from os import listdir
from parameters import Parameters
from data_preprocessing import lemmatize_words
from data_preprocessing import remove_html_tags

def prepare_word2vec_training_data():
    processed_movie_descriptions = read_movie_descriptions()
    processed_game_descriptions = read_game_descriptions()
    processed_book_descriptions = read_book_descriptions()
    processed_movie_reviews = read_movie_reviews()
    return processed_movie_descriptions + processed_game_descriptions + processed_book_descriptions + processed_movie_reviews


def read_movie_descriptions():
    print('Reading movie descriptions...')
    raw_movie_descriptions = []
    with open(f'{Parameters.word2vec_train_data_path}movies_metadata.csv', encoding="utf-8") as movie_metadata_csv:
        csv_reader = csv.reader(movie_metadata_csv, delimiter=',')
        for i, row in enumerate(csv_reader):
            if i != 0:
                raw_movie_descriptions.append(row[9])
    print('Processing movie descriptions...')
    processed_movie_descriptions = [lemmatize_words(simple_preprocess(rmd)) for rmd in raw_movie_descriptions]
    return processed_movie_descriptions


def read_game_descriptions():
    print('Reading game descriptions...')
    raw_game_descriptions = []
    with open(f'{Parameters.word2vec_train_data_path}games_features.csv', encoding="utf-8") as game_features_csv:
        csv_reader = csv.reader(game_features_csv, delimiter=',')
        for i, row in enumerate(csv_reader):
            if i != 0:
                raw_game_descriptions.append(row[61])
    print('Processing game descriptions...')
    processed_game_descriptions = [lemmatize_words(simple_preprocess(rgd)) for rgd in raw_game_descriptions]
    return processed_game_descriptions


def read_book_descriptions():
    print('Reading book descriptions...')
    raw_book_descriptions = []
    with open(f'{Parameters.word2vec_train_data_path}booksummaries.txt', encoding='utf-8') as book_summaries_csv:
        csv_reader = csv.reader(book_summaries_csv, delimiter='\t')
        for i, row in enumerate(csv_reader):
            if i != 0:
                raw_book_descriptions.append(row[6])
    print('Processing book descriptions...')
    processed_book_descriptions = [lemmatize_words(simple_preprocess(rbd)) for rbd in raw_book_descriptions]
    return processed_book_descriptions

def read_movie_reviews():
    print('Reading movie reviews...')
    raw_movie_reviews = []
    file_names = listdir(f'{Parameters.word2vec_train_data_path}unsup')
    for fn in file_names:
        with open(f'{Parameters.word2vec_train_data_path}unsup/{fn}', mode='r', encoding='utf-8') as review_file:
            review_text = review_file.readline()
            raw_movie_reviews.append(review_text)
    print('Processing movie reviews...')
    processed_movie_reviews = []
    for rmr in raw_movie_reviews:
        mr_no_html_tags = remove_html_tags(rmr)
        mr_tokenized = simple_preprocess(mr_no_html_tags)
        mr_lemmatized = lemmatize_words(mr_tokenized)
        processed_movie_reviews.append(mr_lemmatized)
    return processed_movie_reviews
    

def read_game_reviews():
    print('Reading game reviews...')
    raw_game_reviews = []
    processed_game_reviews = []
    print('Processing game reviews...')
    return processed_game_reviews


def word2vec_train(training_documents):
    print('Training model...')
    model = Word2Vec(training_documents, min_count=2, workers=10)
    model.train(training_documents, total_examples=len(training_documents), epochs=10)
    print('Model trained')
    return model


def save_model_vectors(model):
    word_vectors = model.wv
    word_vectors.save(f'{Parameters.generated_data_path}word_vectors.kv')


def main():
    # training_documents = prepare_word2vec_training_data()
    # model = word2vec_train(training_documents)
    # save_model_vectors(model)


if __name__ == '__main__':
    main()
    