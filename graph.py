import numpy as np
import pandas as pd
import load_data as ld
import preprocess as pre
import util
import networkx as nx
import dijkstra as d
import kruskal as k
import PFNET
from textrank import KeywordSummarizer

class KnowledgeGraph:
    
    def __init__(self, title, n_node, scale, edge_option, word_option, cut_option, r):
        self.e_option = edge_option
        self.w_option = word_option
        self.scale = scale
        self.n_node = n_node
        self.paras = ld.read_txt(title + ".txt")
        
        self.nodes = self.get_nodes()
        self.edges = self.get_adj()
        self.G = self.make_graph(self.nodes, self.edges)
        self.cut_G = self.cutting_edge(self.G, self.edges, r, cut_option)
        self.r = util.correlation(self.edges)
            
    def get_nodes(self):
        if self.w_option == "Term-Frequency":
            tokens_comb = pre.preprocess_node(self.paras)
            dic_comb = pre.make_dic_count(tokens_comb)
            return util.get_top_N(dic_comb, self.n_node) 
        elif self.w_option =="TextRank":
            keyword_extractor = KeywordSummarizer(
                tokenize = pre.mecab_tokenize,
                window = -1,
                verbose = False
            )
            dic_comb = []
            sents = " ".join(self.paras).split(". ")
            keywords = keyword_extractor.summarize(sents, topk=self.n_node)
            for word, rank in keywords:
                dic_comb.append((word, round(rank, 2)))
            return dic_comb
                
    def get_adj(self):
        
        tokens_paras, tokens_stcs = pre.preprocess_edge(self.paras) 
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
        
        N = len(self.nodes)
        cotable = np.zeros((N, N))
        
        # tokens_stc : [['녹차', '속', '폴리페놀'], ['거리', '커피', '전문점', '녹차', '전문점'], ... ]
        # tokens_dic : [['녹차', '속', '폴리페놀'], ['거리', '커피', '전문점', '녹차', '전문점', '녹차', '곳', ... ], ... ]
        # dic_Stcs : [{'녹차': 1, '속': 1, '폴리페놀': 1}, {'거리': 1, '커피': 1, '전문점': 2, '녹차': 1},
        # dict_paras : [{'녹차': 1, '속': 1, '폴리페놀': 1}, {'거리': 1, '커피': 1, '전문점': 2, '녹차': 5, '곳': 1, ... ], ... ]        
        
        # upper triangle shape
        for i in range(N):
            for j in range(i+1, N):
                left, right = self.nodes[i][0], self.nodes[j][0]
                if self.e_option == "ss":
                    for stc in tokens_stcs:
                        if left in stc and right in stc:
                            cotable[i][j] += 1        
                elif self.e_option == "ps":
                    for para in tokens_paras:
                        if left in para and right in para:
                            cotable[i][j] += 1  
                elif self.e_option == "scs":
                    Lvector = get_vector(dic_stcs, left)
                    Rvector = get_vector(dic_stcs, right)
                    sim = util.cos_similarity(Lvector, Rvector)
                    if sim != 0:
                        cotable[i][j] = util.rescale(sim, self.scale)
                elif self.e_option == "pcs":
                    Lvector = get_vector(dic_paras, left)
                    Rvector = get_vector(dic_paras, right)
                    sim = util.cos_similarity(Lvector, Rvector)
                    if sim != 0:
                        cotable[i][j] = util.rescale(sim, self.scale)
                else:
                    print("error : choose option among ('ss', 'ps', 'scs', 'pcs')")
        #print("before cotable : ", cotable)
                    
        no_edge_idx = np.where(cotable == 0)
        
        if self.e_option == "ss" or self.e_option == "ps":
            maxvalue = np.max(cotable)
            cotable = util.rescale(cotable / maxvalue, self.scale)
            for i in range(len(no_edge_idx[0])):
                cotable[no_edge_idx[0][i], no_edge_idx[1][i]] = -1
            
        for i in range(len(no_edge_idx[0])):
            cotable[no_edge_idx[0][i], no_edge_idx[1][i]] = -1
            
        cotable = np.round(cotable, 2)
        
        return cotable

    def make_graph(self, nodes, adj):
        G = nx.Graph()
        for i in range(len(nodes)):
            for j in range(i+1, len(nodes)):
                if adj[i][j] != -1:
                    nodei = str(nodes[i][0])+" "+str(nodes[i][1])
                    nodej = str(nodes[j][0])+" "+str(nodes[j][1])
                    G.add_edge(nodei, nodej, weight=adj[i][j])
        return G


    def cutting_edge(self, graph, adj, r, option):

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
                        if dist[i][j] == adj[i][j]:
                            fromN, toN = id2name[i], id2name[j]
                            newG.add_edge(fromN, toN, weight=adj[i][j])

        elif option == "MST":
            parent = k.kruskal(graph, r)
            for p in range(len(parent)):
                fromN, toN = id2name[p], id2name[parent[p]]
                if fromN != toN:
                    w = adj[p][parent[p]] if adj[p][parent[p]] > 0 else adj[parent[p]][p]
                    newG.add_edge(fromN, toN, weight=w)
                    
        elif option == "PFNET":
            if r == float("inf"):
                newG = PFNET.minimal_pathfinder(graph)
            else:
                newG = PFNET.minimal_pathfinder(graph, r)
                
        return newG
