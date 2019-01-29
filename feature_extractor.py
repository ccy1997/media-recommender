import gensim
import numpy as np

def calculate_item_vector(word_list, d, model):
    item_vector = np.zeros(shape=(d,))

    for word in word_list:
        try:
            word_vector = model[word]
            item_vector += word_vector
        except KeyError as e:
            print(e)

    return np.divide(item_vector, len(word_list))
        
