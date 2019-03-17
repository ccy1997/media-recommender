import gensim
import numpy as np
import pandas as pd
import csv
import data_preprocessing
from parameters import Parameters


def calculate_item_vector(word_list, d, model):
    item_vector = np.zeros(shape=(d,))

    for word in word_list:
        try:
            word_vector = model[word]
            item_vector += word_vector
        except KeyError as e:
            print(e)

    return np.divide(item_vector, len(word_list))


def vectorize_items(in_file_str, out_file_str, model):
    item_df = pd.read_csv('./' + in_file_str)
    item_df.set_index('id', inplace=True)

    for i, row in item_df.iterrows():
        print(f'Vectorizing {in_file_str}: item_id = {str(i)}')
        word_list = row['words'].split(' ')
        item_df.at[i, 'words'] = np.array2string(calculate_item_vector(word_list, model.vector_size, model)).strip(' []')

    item_df.rename(columns = {'words':'vector'}, inplace=True)
    item_df.to_csv(out_file_str, sep=',', encoding='utf-8')


def prepare_word2vec_training_data():
    # Prepare movie description
    raw_movie_descriptions = []
    with open('./data/word2vec_train/movies_metadata.csv', encoding="utf-8") as movie_metadata_csv:
        csv_reader = csv.reader(movie_metadata_csv, delimiter=',')
        for i, row in enumerate(csv_reader):
            if i != 0:
                raw_movie_descriptions.append(row[9])
    processed_movie_descriptions = [data_preprocessing.lemmatize_words(gensim.utils.simple_preprocess(rmd)) for rmd in raw_movie_descriptions]

    # Prepare game description
    raw_game_descriptions = []
    with open('./data/word2vec_train/games_features.csv', encoding="utf-8") as game_features_csv:
        csv_reader = csv.reader(game_features_csv, delimiter=',')
        for i, row in enumerate(csv_reader):
            if i != 0:
                raw_game_descriptions.append(row[61])
    processed_game_descriptions = [data_preprocessing.lemmatize_words(gensim.utils.simple_preprocess(rgd)) for rgd in raw_game_descriptions]

    # Prepare book description
    raw_book_descriptions = []
    with open('./data/word2vec_train/booksummaries.txt', encoding='utf-8') as book_summaries_csv:
        csv_reader = csv.reader(book_summaries_csv, delimiter='\t')
        for i, row in enumerate(csv_reader):
            if i != 0:
                raw_book_descriptions.append(row[6])
    processed_book_descriptions = [data_preprocessing.lemmatize_words(gensim.utils.simple_preprocess(rbd)) for rbd in raw_book_descriptions]

    return processed_movie_descriptions + processed_game_descriptions + processed_book_descriptions


def main():
    print('Training model...')
    # model = gensim.models.KeyedVectors.load_word2vec_format( './GoogleNews-vectors-negative300.bin', binary=True)
    training_documents = prepare_word2vec_training_data()
    model = gensim.models.Word2Vec(training_documents, size=50, window=10, min_count=2, workers=10)
    model.train(training_documents, total_examples=len(training_documents), epochs=10)
    print('Model trained')

    # Vectorize items by corresponding keywords
    vectorize_items(Parameters.generated_data_path + Parameters.preprocessed_movie_csv_name, 
                    Parameters.generated_data_path + Parameters.vectorized_movie_csv_name, model)
    vectorize_items(Parameters.generated_data_path + Parameters.preprocessed_game_csv_name, 
                    Parameters.generated_data_path + Parameters.vectorized_game_csv_name, model)
    vectorize_items(Parameters.generated_data_path + Parameters.preprocessed_book_csv_name, 
                    Parameters.generated_data_path + Parameters.vectorized_book_csv_name, model)


if __name__ == '__main__':
    main()