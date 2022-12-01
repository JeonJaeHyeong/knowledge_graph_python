import heapq
import numpy as np

# 우선순위 큐 활용
def dijkstra(graph, r):
    
    nodes = graph.nodes
    node2idx = {}
    idx2node = {}
    
    for idx, n in enumerate(nodes):
        node2idx[n] = idx 
        idx2node[idx] = n
        
    distances = [ [float('inf') for _ in range(len(nodes))] for _ in range(len(nodes))]
    for i in range(len(nodes)):
        distances[i][i] = 0    

    parents = [{} for _ in range(len(nodes))]
            
    for n in nodes:

        nidx = node2idx[n]
        queue = []
        heapq.heappush(queue, [0, nidx])

        for c in range(0, len(nodes)):
            if c != nidx:
                parents[nidx][c] = None
    
        while queue:
            curr_distance, curridx = heapq.heappop(queue)
            if distances[nidx][curridx] < curr_distance:
                continue
            
            curr = idx2node[curridx]
            for nei in graph.neighbors(curr):
                
                neidx = node2idx[nei]
                if neidx == nidx:
                    continue
                if r == float("inf"):
                    distance = max(curr_distance, graph[curr][nei]['weight'])
                else:
                    distance = np.power(np.power(curr_distance, r) + np.power(graph[curr][nei]['weight'], r), 1/r)

                if distance < distances[nidx][neidx]:
                    distances[nidx][neidx] = distance
                    heapq.heappush(queue, [distance, neidx])
                    parents[nidx][neidx] = curridx
                    
    return distances, parents