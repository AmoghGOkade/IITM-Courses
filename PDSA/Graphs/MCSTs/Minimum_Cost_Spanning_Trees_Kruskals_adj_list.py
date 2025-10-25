def kruskal(Wlist):
    edges = []
    component = {}
    tree_edges = []
    for u in Wlist.keys():
        '''edges.extend([(d, u, v) for (v, d) in Wlist[u]])'''
        for (v, d) in Wlist[u]:
            edges.append((d, u, v))
            
        component[u] = u
        
    edges.sort()    # we have used the weight as the 1st index in edges, so it gets sorted based on that

    for (d, u, v) in edges:
        if component[u] != component[v]:    #edge doesn't create a cycle
            tree_edges.append((u, v))
            c = component[u]        #can't write component[u] instead of c in the bottom line because component[u] might get changed before changing all nodes that have component[u]
            for i in Wlist.keys():
                if component[i] == c:   #if a node is of component u, change it to component v
                    component[i] = component[v]

    return tree_edges
