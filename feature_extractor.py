import gensim
import numpy as np
import pandas as pd
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
        print( 'Vectorizing {}: id = {}'.format(in_file_str, str(i)) )
        word_list = row['words'].split(' ')
        item_df.at[i, 'words'] = np.array2string(calculate_item_vector(word_list, model.vector_size, model)).strip(' []')

    item_df.rename(columns = {'words':'vector'}, inplace=True)
    item_df.to_csv(out_file_str, sep=',', encoding='utf-8')


def main():
    # Load pre-trained model based on google news dataset
    print('Loading model...')
    model = gensim.models.KeyedVectors.load_word2vec_format( './GoogleNews-vectors-negative300.bin', binary=True)

    # Vectorize items by corresponding keywords
    vectorize_items(Parameters.data_folder_path + Parameters.preprocessed_movie_csv_name, 
                    Parameters.data_folder_path + Parameters.vectorized_movie_csv_name, model)
    vectorize_items(Parameters.data_folder_path + Parameters.preprocessed_game_csv_name, 
                    Parameters.data_folder_path + Parameters.vectorized_game_csv_name, model)
    vectorize_items(Parameters.data_folder_path + Parameters.preprocessed_book_csv_name, 
                    Parameters.data_folder_path + Parameters.vectorized_book_csv_name, model)


if __name__ == '__main__':
    main()