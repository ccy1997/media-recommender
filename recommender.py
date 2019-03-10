from enum import Enum
from sklearn.neighbors import NearestNeighbors
import numpy as np
import pandas as pd
from collections import Counter
from parameters import Parameters

class Media(Enum):
    MOVIE = 'Movie'
    GAME = 'Game'
    BOOK = 'Book'


class Recommender:
    def __init__(self, movies_df, games_df, books_df, user_favorites_df):
        self.movies_df = movies_df
        self.games_df = games_df
        self.books_df = books_df
        self.user_favorites_df = user_favorites_df
        self.user_vector = self.__user_favorites_to_user_vector()

    def generate_k_recommendations(self, media_type, k):
        item_vectors = []

        if media_type == Media.MOVIE:
            movies_df_no_favorites = self.__remove_favorites_from_item_df(Media.MOVIE)
            item_vectors = np.stack(movies_df_no_favorites['vector'].values)
        elif media_type == Media.GAME:
            games_df_no_favorites = self.__remove_favorites_from_item_df(Media.GAME)
            item_vectors = np.stack(games_df_no_favorites['vector'].values)
        elif media_type == Media.BOOK:
            books_df_no_favorites = self.__remove_favorites_from_item_df(Media.BOOK)
            item_vectors = np.stack(books_df_no_favorites['vector'].values)
        else:
            print('Unknown media type: generate_k_recommendations')
            return

        nbrs = NearestNeighbors(n_neighbors=k, algorithm='auto').fit(item_vectors)
        _, indices = nbrs.kneighbors(self.user_vector)
        
        if media_type == Media.MOVIE:
            return movies_df_no_favorites.iloc[indices[0]]['title']
        elif media_type == Media.GAME:
            return games_df_no_favorites.iloc[indices[0]]['title']
        elif media_type == Media.BOOK:
            return books_df_no_favorites.iloc[indices[0]]['title']
        else:
            print('Unknown media type: generate_k_recommendations')
            return

    def __user_favorites_to_user_vector(self):
        favorite_vectors = []
        
        for _, row in self.user_favorites_df.iterrows():

            if Media(row['type']) == Media.MOVIE:
                favorite_vectors.append(self.movies_df.at[row['item_id'], 'vector'])
            elif Media(row['type']) == Media.GAME:
                favorite_vectors.append(self.games_df.at[row['item_id'], 'vector'])
            elif Media(row['type']) == Media.BOOK:
                favorite_vectors.append(self.books_df.at[row['item_id'], 'vector'])
            else:
                print('Unknown media type: extract_user_vectors')
                return

        return np.mean(np.asarray(favorite_vectors), axis=0).reshape(1, -1)

    def __remove_favorites_from_item_df(self, media_type):
        if (media_type == Media.MOVIE):
            remove_indices = self.user_favorites_df.loc[self.user_favorites_df['type'] == 'Movie', ['item_id']].values.ravel()
            return self.movies_df.drop(remove_indices)
        elif (media_type == Media.GAME):
            remove_indices = self.user_favorites_df.loc[self.user_favorites_df['type'] == 'Game', ['item_id']].values.ravel()
            return self.games_df.drop(remove_indices)
        elif (media_type == Media.BOOK):
            remove_indices = self.user_favorites_df.loc[self.user_favorites_df['type'] == 'Book', ['item_id']].values.ravel()
            return self.books_df.drop(remove_indices)
        else:
            print('Unknown media type: __remove_favorites_from_item_dfs')
            return

def read_vectorized_items(in_file_name):
    item_df = pd.read_csv('./' + in_file_name)
    item_df.set_index('id', inplace=True)
    item_df['vector'] = [np.fromstring(row['vector'], dtype=float, sep=' ') for i, row in item_df.iterrows()]
    return item_df


def main():
    # Read item's data
    movies_df = read_vectorized_items(Parameters.data_folder_path + Parameters.vectorized_movie_csv_name)
    games_df = read_vectorized_items(Parameters.data_folder_path + Parameters.vectorized_game_csv_name)
    books_df = read_vectorized_items(Parameters.data_folder_path + Parameters.vectorized_book_csv_name)
    
    # Read user favorites
    user_favorites_df = pd.read_csv(Parameters.data_folder_path + Parameters.user_favorites_csv_name)

    # Create a Recommender object
    r = Recommender(movies_df, games_df, books_df, user_favorites_df)

    # Generate recommendation
    movie_recommendation = r.generate_k_recommendations(Media.MOVIE, 1)
    print('Movies recommendation: ')
    print(movie_recommendation)

    game_recommendation = r.generate_k_recommendations(Media.GAME, 2)
    print('\nGames recommendation: ')
    print(game_recommendation)

    book_recommendation = r.generate_k_recommendations(Media.BOOK, 5)
    print('\nBooks recommendation: ')
    print(book_recommendation)
    

if __name__ == '__main__':
    main()
