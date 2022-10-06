import numpy as np
import pandas as pd
import load_data as ld
import preprocess as pre
from numpy.linalg import norm

def cos_similarity(lst1, lst2):
    return np.dot(lst1, lst2)/(norm(lst1)*norm(lst2))

def get_top_N(dict, n):
    sorted_dict = sorted(dict, key = dict.get, reverse=True)[:n]
    return sorted_dict

def make_graph(paragraphs, option):
    
    nouns_comb, nouns_paras, nouns_stcs = pre.preprocessing(paragraphs) 
    dic_comb = pre.make_dic_count(nouns_comb)
    dic_paras = list(map(pre.make_dic_count, nouns_paras))
    dic_stcs = list(map(pre.get_stcs_dic, nouns_stcs))

    nouns_stcs = sum(nouns_stcs, [])
    dic_stcs = sum(dic_stcs, [])
    TopNList = get_top_N(dic_comb, 10) 
    
    def get_vector(dictList, keyword):
        vector = []
        for dic in dictList:
            if keyword in dic.keys():
                vector.append(dic[keyword])
            else:
                vector.append(0)
        return vector
    
    N = len(TopNList)
    cotable = np.zeros((N, N))
        
    
    for i in range(N):
        for j in range(N):
            left, right = TopNList[i], TopNList[j]
            if option == "ss":
                for stc in nouns_stcs:
                    if left in stc and right in stc:
                        cotable[i][j] += 1        
            elif option == "ps":
                for para in nouns_paras:
                    if left in para and right in para:
                        cotable[i][j] += 1  
            elif option == "scs":
                Lvector = get_vector(dic_stcs, left)
                Rvector = get_vector(dic_stcs, right)
                cotable[i][j] = cos_similarity(Lvector, Rvector)
            elif option == "pcs":
                Lvector = get_vector(dic_paras, left)
                Rvector = get_vector(dic_paras, right)
                cotable[i][j] = cos_similarity(Lvector, Rvector)
            else:
                print("error : choose option among ('ss', 'ps', 'scs', 'pcs')")
    return cotable