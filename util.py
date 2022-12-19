import numpy as np
import operator

def cos_similarity(lst1, lst2):
    return np.dot(lst1, lst2)/(np.linalg.norm(lst1)*np.linalg.norm(lst2))

def rescale(num, scale):
    return scale - (scale-1)*num

def correlation(adj):

    return 0

def get_top_N(dict, n_node):
    sorted_dict = sorted(dict.items(), key=operator.itemgetter(1), reverse=True)[:n_node]
    return sorted_dict
