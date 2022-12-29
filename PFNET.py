def minimal_pathfinder(G, r = float("inf")):
    """ 
    Args:
    -----
    G [networkX graph]:
        Graph to filter links from.
    r [float]:
        "r" parameter as in the paper.

    Returns:
    -----
    PFNET [networkX graph]:
        Graph containing only the PFNET links.
    """
    
    import networkx as nx
    from collections import defaultdict
    
    H = G.copy()
    
    # Initialize adjacency matrix W
    W = defaultdict(lambda: defaultdict(lambda: float("inf")))
    
    # Set diagonal to 0
    for u in H.nodes():
        W[u][u] = 0 
    
    # Get weights and set W values
    for i, j, d in H.edges(data=True):
        W[i][j] = d['weight'] # Add weights to W
        
    # Get shortest path distance matrix D
    dist = nx.floyd_warshall_predecessor_and_distance(H, weight='weight')[1]
    
    # Iterate over all triples to get values for D
    for k in H.nodes():
        for i in H.nodes():
            for j in H.nodes():
                if r == float("inf"): # adapted from the R-comato version which does a similar check
                # Discard non-shortest paths
                    dist[i][j] = min(dist[i][j], max(dist[i][k], dist[k][j]))
                else:
                    dist[i][j] = min(dist[i][j], (((dist[i][k]) ** r) + ((dist[k][j]) ** r )) ** (1/r))
                
    # Check for type; set placeholder for either case
    if not H.is_directed():
        PFNET = nx.Graph()
        PFNET.add_nodes_from(H.nodes(data=True))
    else:
        PFNET = nx.DiGraph()
        PFNET.add_nodes_from(H.nodes(data=True))
        
    # Add links D_ij only if == W_ij
    for i in H.nodes():
        for j in H.nodes():
            if dist[i][j] == W[i][j]: # If shortest path distance equals distance in adjacency
                if dist[i][j] == float("inf"): # Skip infinite path lengths
                    pass
                elif i == j: # Skip the diagonal
                    pass
                else: # Add link to PFNET
                    weight = dist[i][j]
                    PFNET.add_edge(i, j, weight=weight)
                    
    return PFNET