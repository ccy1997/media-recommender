from sklearn.neighbors import NearestNeighbors
import numpy as np

def generate_k_recommendations(user_vector, item_vectors, items, k):
    nbrs = NearestNeighbors(n_neighbors=k, algorithm='auto').fit(item_vectors)
    distances, indices = nbrs.kneighbors(user_vector)
    print('Recommendation:')

    for i in indices[0]:
        print(str(items.index[i]) + ' ' + items.iloc[i]['name'])
        
