from gensim.models import KeyedVectors
import numpy as np
import pandas as pd
import csv
import data_preprocessing
from parameters import Parameters


def calculate_item_vector(word_list, d, word_vectors):
    item_vector = np.zeros(shape=(d,))

    for word in word_list:
        try:
            word_vector = word_vectors[word]
            item_vector += word_vector
        except KeyError as e:
            print(e)

    return np.divide(item_vector, len(word_list))


def vectorize_items(in_file_str, out_file_str, word_vectors):
    item_df = pd.read_csv('./' + in_file_str)
    item_df.set_index('id', inplace=True)

    for i, row in item_df.iterrows():
        print(f'Vectorizing {in_file_str}: item_id = {str(i)}')
        word_list = row['words'].split(' ')
        item_df.at[i, 'words'] = np.array2string(calculate_item_vector(word_list, word_vectors.vector_size, word_vectors)).strip(' []')

    item_df.rename(columns = {'words':'vector'}, inplace=True)
    item_df.to_csv(out_file_str, sep=',', encoding='utf-8')


def main():
    # Load trained word vectors
    print('Loading trained word vectors...')
    word_vectors = KeyedVectors.load(f'{Parameters.generated_data_path}word_vectors.kv', mmap='r')
    # word_vectors = KeyedVectors.load_word2vec_format(f'{Parameters.word2vec_train_data_path}GoogleNews-vectors-negative300.bin', binary=True)
    print('Word vectors loaded')

    # Vectorize items by their corresponding keywords
    vectorize_items(Parameters.generated_data_path + Parameters.preprocessed_movie_csv_name, 
                    Parameters.generated_data_path + Parameters.vectorized_movie_csv_name, word_vectors)
    vectorize_items(Parameters.generated_data_path + Parameters.preprocessed_game_csv_name, 
                    Parameters.generated_data_path + Parameters.vectorized_game_csv_name, word_vectors)
    vectorize_items(Parameters.generated_data_path + Parameters.preprocessed_book_csv_name, 
                    Parameters.generated_data_path + Parameters.vectorized_book_csv_name, word_vectors)


if __name__ == '__main__':
    main()