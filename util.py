import numpy as np
import operator
from scipy.stats import pearsonr, linregress

graph_sim = 0
common_nodes = []
common_edges = []

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

def graph_similarity(g1, g2):
    
    global graph_sim, common_edges, common_nodes

    node1 = [ name for (name, weight) in g1.nodes]
    node2 = [ name for (name, weight) in g2.nodes]
    common_nodes = list(set(node1) & set(node2))

    idx1, idx2 = [], []
    for c_node in common_nodes:
        idx1.append(node1.index(c_node))
        idx2.append(node2.index(c_node))

    edge1, edge2 = g1.cut_G.edges, g2.cut_G.edges
    edge1 = [ (n1.split()[0], n2.split()[0]) for (n1, n2) in edge1 ]
    edge2 = [ (n1.split()[0], n2.split()[0]) for (n1, n2) in edge2 ]

    common_edges = list(set(edge1) & set(edge2))
    graph_sim = len(common_edges) / max(len(edge1), len(edge2))


def get_top_N(dict, n_node):
    #dict = user_define_dict(dict)
    sorted_dict = sorted(dict.items(), key=operator.itemgetter(1), reverse=True)[:n_node]
    return sorted_dict

def user_define_dict(dict):
    temp_dict = {}
#    temp_dict['통계학연구원'] = dict['통계학연구원']
#    temp_dict['수학과'] = dict['수학과']
#    temp_dict['통계학과'] = dict['통계학과']
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

    temp_dict['공통수학1'] = dict['공통수학1']
    temp_dict['공통수학2'] = dict['공통수학2']
    temp_dict['기본수학1'] = dict['기본수학1']
    temp_dict['기본수학2'] = dict['기본수학2']
    temp_dict['대수'] = dict['대수']
#    temp_dict['미적분Ⅰ'] = dict['미적분Ⅰ']
    temp_dict['확률과 통계'] = dict['확률과 통계']
    temp_dict['기하'] = dict['기하']
    temp_dict['경제 수학'] = dict['경제 수학']
    temp_dict['인공지능 수학'] = dict['인공지능 수학']
    temp_dict['직무 수학'] = dict['직무 수학']
    return temp_dict
