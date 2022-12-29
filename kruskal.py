import numpy as np

# 우선순위 큐 활용
def kruskal(graph, r):
    
    nodes = graph.nodes
    edges = []
    node2idx = {}
    idx2node = {}
    result = 0
    
    # 특정 원소가 속한 집합 찾기
    def root(parent, x):
        if parent[x] == x:
            return x
        parent[x] = root(parent, parent[x])
        return parent[x]
        
    # 두 원소가 속한 집합 찾기
    def union(parent, a, b):
        rootA = root(parent, a)
        rootB = root(parent, b)
        
        if rootA < rootB:
            parent[rootB] = rootA
        else:
            parent[rootA] = rootB

    
    for idx, n in enumerate(nodes):
        node2idx[n] = idx 
        idx2node[idx] = n

    parent = [i for i in range(len(nodes))]

    for (u, v, w) in graph.edges(data=True):
        uidx = node2idx[u]
        vidx = node2idx[v]
        edges.append((w['weight'], uidx, vidx))
        
    edges.sort()
                    
    for (cost, u, v) in edges:
        if root(parent, u) != root(parent, v):
            union(parent, u, v)
            result += cost        
                    
    return parent