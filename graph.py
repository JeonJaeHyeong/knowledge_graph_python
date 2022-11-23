import numpy as np
import pandas as pd
import load_data as ld
import preprocess as pre
from numpy.linalg import norm
import networkx as nx
import operator
import dijkstra as d
import kruskal as k
import PFNET
from textrank import KeywordSummarizer


def cos_similarity(lst1, lst2):
    return np.dot(lst1, lst2)/(np.linalg.norm(lst1)*np.linalg.norm(lst2))

def rescale(num, maxNum):
    return maxNum - (maxNum-1)*num

def get_top_N(dict, n):
    tmp_dict = {}
    sorted_dict = sorted(dict.items(), key=operator.itemgetter(1), reverse=True)[:n] #sorted(dict, key = dict.get, reverse=True)[:n]
    #print("dict : ", dict)
    
    tmp_dict['카테친'] = dict['카테친'] 
    tmp_dict['추출물'] = dict['추출물'] 
    tmp_dict['유도체'] = dict['유도체'] 
    tmp_dict['찻잎'] = dict['찻잎'] 
    tmp_dict['억제'] = dict['억제'] 
    tmp_dict['암세포'] = dict['암세포'] 
    tmp_dict['유로키나제'] = dict['유로키나제'] 
    tmp_dict['녹차'] = dict['녹차'] 
    tmp_dict['효능'] = dict['효능'] 
    tmp_dict['차'] = dict['차'] 
    tmp_dict['화학물질'] = dict['화학물질'] 
    tmp_dict['폴리페놀'] = dict['폴리페놀'] 
    tmp_dict['플라반올'] = dict['플라반올'] 
    tmp_dict['테아플라빈'] = dict['테아플라빈'] 
    
    
    '''
    tmp_dict['카테킨'] = dict['카테킨'] 
    tmp_dict['자일리톨'] = dict['자일리톨'] 
    tmp_dict['비타민'] = dict['비타민'] 
    tmp_dict['증상'] = dict['증상'] 
    tmp_dict['감염'] = dict['감염'] 
    tmp_dict['독감'] = dict['독감'] 
    tmp_dict['바이러스'] = dict['바이러스'] 
    tmp_dict['녹차'] = dict['녹차'] 
    tmp_dict['섭취'] = dict['섭취'] 
    tmp_dict['차'] = dict['차'] 
    tmp_dict['알파파'] = dict['알파파'] 
    tmp_dict['데아닌'] = dict['데아닌'] 
    tmp_dict['이뇨작용'] = dict['이뇨작용'] 
    tmp_dict['감기'] = dict['감기'] 
    '''
    tmp_dict = sorted(tmp_dict.items(), key=operator.itemgetter(1), reverse=True)
    print("tmp : ", tmp_dict)
    
    return tmp_dict #sorted_dict

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb
    
    
def get_nodes(title, option="TF", n=10):
    paragraphs = ld.read_txt(title + ".txt")
    if option=="TF":
        tokens_comb = pre.preprocess_node(paragraphs)
        dic_comb = pre.make_dic_count(tokens_comb)
        return get_top_N(dic_comb, n) 
    elif option=="textrank":
        keyword_extractor = KeywordSummarizer(
            tokenize = pre.mecab_tokenize,
            window = -1,
            verbose = False
        )
        dic_comb = []
        sents = " ".join(paragraphs).split(". ")
        keywords = keyword_extractor.summarize(sents, topk=n)
        for word, rank in keywords:
            dic_comb.append((word, rank))
        return dic_comb
            

def get_adj(title, nodes, option, scale):
    
    paragraphs = ld.read_txt(title + ".txt")
    tokens_paras, tokens_stcs = pre.preprocess_edge(paragraphs) 
    dic_paras = list(map(pre.make_dic_count, tokens_paras))
    dic_stcs = list(map(pre.get_stcs_dic, tokens_stcs))
    
    tokens_stcs = sum(tokens_stcs, [])
    dic_stcs = sum(dic_stcs, [])
    
    def get_vector(dictList, keyword):
        vector = []
        for dic in dictList:
            if keyword in dic.keys():
                vector.append(dic[keyword])
            else:
                vector.append(0)
        return vector
    
    N = len(nodes)
    cotable = np.zeros((N, N))
    
    # tokens_stc : [['녹차', '속', '폴리페놀'], ['거리', '커피', '전문점', '녹차', '전문점'], ... ]
    # tokens_dic : [['녹차', '속', '폴리페놀'], ['거리', '커피', '전문점', '녹차', '전문점', '녹차', '곳', ... ], ... ]
    # dic_Stcs : [{'녹차': 1, '속': 1, '폴리페놀': 1}, {'거리': 1, '커피': 1, '전문점': 2, '녹차': 1},
    # dict_paras : [{'녹차': 1, '속': 1, '폴리페놀': 1}, {'거리': 1, '커피': 1, '전문점': 2, '녹차': 5, '곳': 1, ... ], ... ]        
    
    for i in range(N):
        for j in range(i+1, N):
            left, right = nodes[i][0], nodes[j][0]
            if option == "ss":
                for stc in tokens_stcs:
                    if left in stc and right in stc:
                        cotable[i][j] += 1        
            elif option == "ps":
                for para in tokens_paras:
                    if left in para and right in para:
                        cotable[i][j] += 1  
            elif option == "scs":
                Lvector = get_vector(dic_stcs, left)
                Rvector = get_vector(dic_stcs, right)
                sim = cos_similarity(Lvector, Rvector)
                if sim != 0:
                    cotable[i][j] = rescale(cos_similarity(Lvector, Rvector), scale)
            elif option == "pcs":
                Lvector = get_vector(dic_paras, left)
                Rvector = get_vector(dic_paras, right)
                sim = cos_similarity(Lvector, Rvector)
                if sim != 0:
                    cotable[i][j] = rescale(cos_similarity(Lvector, Rvector), scale)
            else:
                print("error : choose option among ('ss', 'ps', 'scs', 'pcs')")
    #print("before cotable : ", cotable)
                
    no_edge_idx = np.where(cotable == 0)
    
    if option == "ss" or option == "ps":
        maxvalue = np.max(cotable)
        cotable = rescale(cotable / maxvalue, scale)
        for i in range(len(no_edge_idx[0])):
            cotable[no_edge_idx[0][i], no_edge_idx[1][i]] = -1
        
    for i in range(len(no_edge_idx[0])):
        cotable[no_edge_idx[0][i], no_edge_idx[1][i]] = -1
        
    cotable = np.round(cotable, 2)
    
    return cotable

def make_graph(nodes, adj):
    G = nx.Graph()
    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            if adj[i][j] != -1:
                nodei = str(nodes[i][0])+" "+str(nodes[i][1])
                nodej = str(nodes[j][0])+" "+str(nodes[j][1])
                G.add_edge(nodei, nodej, weight=adj[i][j])
    return G

def get_route(parent, start, end):
    route = []
    current = end
    while current != start:
        route.append(current)
        current = parent[current]
    
    route.append(start)
    route.reverse()
    return route 

def cutting_edge(graph, adj, r, option):

    nodes = list(graph.nodes)
    n = len(nodes)
    newG = nx.Graph()
    id2name = {}
    for idx, name in enumerate(nodes):
        id2name[idx] = name

    if option == "dijkstra":
        dist, parents = d.dijkstra(graph, r)
        for i in range(n):
            for j in range(i+1, n):
                if dist[i][j] != float('inf'):
                    route = get_route(parents[i], i, j)
                    for p in range(len(route)-1):
                        fromN, toN = id2name[route[p]], id2name[route[p+1]]
                        if not newG.has_edge(fromN, toN):
                            newG.add_edge(fromN, toN, weight=adj[route[p]][route[p+1]])

    elif option == "kruskal":
        parent = k.kruskal(graph, r)
        for p in range(len(parent)):
            fromN, toN = id2name[p], id2name[parent[p]]
            if fromN != toN:
                newG.add_edge(fromN, toN, weight=adj[p][parent[p]])
                
    elif option == "PFNET":
        if r == float("inf"):
            newG = PFNET.minimal_pathfinder(graph)
        else:
            newG = PFNET.minimal_pathfinder(graph, r)
            
    return newG