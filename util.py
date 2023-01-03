import numpy as np
import operator
from scipy.stats import pearsonr, linregress

def cos_similarity(lst1, lst2):
    return np.dot(lst1, lst2)/(np.linalg.norm(lst1)*np.linalg.norm(lst2))

def rescale(num, scale):
    return scale - (scale-1)*num

def correlation(adj):

    sym_adj = adj + adj.T - np.diag(np.diag(adj))

    n, _ = adj.shape
    if n <= 4:
        return None

    indirect = np.zeros((n, n))
    for i in range(n):
        for j in range(i+1, n):
            a, b = sym_adj[i, :], sym_adj[j, :]
            ar, br = np.delete(a, [i, j]), np.delete(b, [i, j])
            indirect[i, j] = linregress(ar, br).rvalue

    size = np.count_nonzero(adj)
    x_xp = adj - np.sum(adj) / size
    y_yp = indirect - np.sum(indirect) / size
    for i in range(n):
        for j in range(i+1):
            x_xp[i, j] = y_yp[i, j] = 0

    x2, y2 = np.sqrt(np.sum(x_xp * x_xp)), np.sqrt(np.sum(y_yp * y_yp))
    r = np.sum(x_xp * y_yp) / (x2 * y2)

    return r

def get_top_N(dict, n_node):
    dict = user_define_dict(dict)
    sorted_dict = sorted(dict.items(), key=operator.itemgetter(1), reverse=True)[:n_node]

    return sorted_dict

def user_define_dict(dict):
    temp_dict = {}
    temp_dict['통계학연구원'] = dict['통계학연구원']
    temp_dict['수학과'] = dict['수학과']
    temp_dict['통계학과'] = dict['통계학과']
    #temp_dict['수학'] = dict['국어']
    #temp_dict['과학'] = dict['과학']
    #temp_dict['물리학'] = dict['물리학']
    #temp_dict['생명'] = dict['생명']
    #temp_dict['화학'] = dict['화학']
    #temp_dict['영어'] = dict['영어']
    #temp_dict['국어'] = dict['국어']
    #temp_dict['미적분'] = dict['미적분']
    #temp_dict['확률'] = dict['확률']
    #temp_dict['통계'] = dict['통계']
    return temp_dict
