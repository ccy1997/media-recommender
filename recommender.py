from enum import Enum
from sklearn.neighbors import NearestNeighbors
import numpy as np
import pandas as pd
from collections import Counter


class Media(Enum):
    MOVIE = 'movie'
    GAME = 'game'
    BOOK = 'book'


class Recommender:
    def __init__(self, movies_df, games_df, books_df, users_ratings_df):
        self.movies_df = movies_df
        self.games_df = games_df
        self.books_df = books_df
        self.users_ratings_df = users_ratings_df
        self.users_vector_df = self.__users_ratings_to_users_vectors()

    def generate_k_recommendations(self, media_type, users_vector, k):
        item_vectors = []

        if media_type == Media.MOVIE:
            item_vectors = np.stack(self.movies_df['documents'].values)
        elif media_type == Media.GAME:
            item_vectors = np.stack(self.games_df['documents'].values)
        elif media_type == Media.BOOK:
            item_vectors = np.stack(self.books_df['documents'].values)
        else:
            print('Unknown media type: generate_k_recommendations')
            return

        nbrs = NearestNeighbors(n_neighbors=k, algorithm='auto').fit(item_vectors)
        _, indices = nbrs.kneighbors(users_vector)
        
        if media_type == Media.MOVIE:
            return [self.movies_df.loc[result]['title'] for result in indices]
        elif media_type == Media.GAME:
            return [self.games_df.loc[result]['title'] for result in indices]
        elif media_type == Media.BOOK:
            return [self.books_df.loc[result]['title'] for result in indices]
        else:
            print('Unknown media type: generate_k_recommendations')
            return

    def __users_ratings_to_users_vectors(self):
        user_vector_df = pd.DataFrame(columns=['id', 'vector'])
        
        for _, row in self.users_ratings_df.iterrows():
            item_vector = []

            if Media(row['type']) == Media.MOVIE:
                item_vector = self.movies_df.at[row['item_id'], 'documents']
            elif Media(row['type']) == Media.GAME:
                item_vector = self.games_df.at[row['item_id'], 'documents']
            elif Media(row['type']) == Media.BOOK:
                item_vector = self.books_df.at[row['item_id'], 'documents']
            else:
                print('Unknown media type: extract_user_vectors')
                return

            user_vector_df.loc[len(user_vector_df)] = [row['user_id'], item_vector]
        
        user_vector_df = user_vector_df.groupby(['id']).apply(np.mean)
        user_vector_df['id'] = user_vector_df['id'].astype(int)
        user_vector_df.set_index('id', inplace=True)
        return user_vector_df

    def print_recommendation_list(self, recommendation_list):
        for user_loc_index, user_recommendation_df in enumerate(recommendation_list):
            print( 'User ID: {}'.format(str(self.users_vector_df.index[user_loc_index])) )
        
            for item_index, row in user_recommendation_df.iteritems():
                print( '{} {}'.format(str(item_index), row) )
   

def read_vectorized_items(in_file_name):
    item_df = pd.read_csv('./' + in_file_name)
    item_df.set_index('id', inplace=True)
    item_df['documents'] = [np.fromstring(row['documents'], dtype=float, sep=' ') for i, row in item_df.iterrows()]
    return item_df


def main():
    # Read item's data
    movies_df = read_vectorized_items('vectorized_movies.csv')
    games_df = read_vectorized_items('vectorized_games.csv')
    books_df = read_vectorized_items('vectorized_books.csv')
    
    # Read user rating's data
    users_ratings_df = pd.read_csv('./users_ratings.csv')

    # Create a Recommender object
    recommender = Recommender(movies_df, games_df, books_df, users_ratings_df)

    # Extract user vectors
    users_vector_array = np.stack(recommender.users_vector_df['vector'].values)

    # Generate recommendation
    movie_recommendations_list = recommender.generate_k_recommendations(Media.MOVIE, users_vector_array, 1)
    print('Movies recommendation: ')
    recommender.print_recommendation_list(movie_recommendations_list)

    game_recommendations_list = recommender.generate_k_recommendations(Media.GAME, users_vector_array, 2)
    print('\nGames recommendation: ')
    recommender.print_recommendation_list(game_recommendations_list)

    book_recommendations_list = recommender.generate_k_recommendations(Media.BOOK, users_vector_array, 5)
    print('\nBooks recommendation: ')
    recommender.print_recommendation_list(book_recommendations_list)
    

if __name__ == '__main__':
    main()
