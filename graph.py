import numpy as np
import pandas as pd
import load_data as ld
import preprocess as pre
from numpy.linalg import norm
import networkx as nx
import operator
from textrank import KeywordSummarizer


def cos_similarity(lst1, lst2):
    return np.dot(lst1, lst2)/(norm(lst1)*norm(lst2))

def rescale(num, maxNum):
    return maxNum*num

def get_top_N(dict, n):
    sorted_dict = sorted(dict.items(), key=operator.itemgetter(1), reverse=True)[:n] #sorted(dict, key = dict.get, reverse=True)[:n]
    return sorted_dict

    
    
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
        
    
    for i in range(N):
        for j in range(N):
            if (i!=j):
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
                    cotable[i][j] = rescale(cos_similarity(Lvector, Rvector), scale)
                elif option == "pcs":
                    Lvector = get_vector(dic_paras, left)
                    Rvector = get_vector(dic_paras, right)
                    cotable[i][j] = rescale(cos_similarity(Lvector, Rvector), scale)
                else:
                    print("error : choose option among ('ss', 'ps', 'scs', 'pcs')")
    if option == "ss" or "ps":
        maxvalue = np.max(cotable)
        cotable = rescale(cotable / maxvalue, scale)
    return cotable