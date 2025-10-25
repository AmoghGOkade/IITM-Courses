def prims(Wlist):
    inf = 1 + max([d for u in Wlist.keys()
                       for (v,d) in Wlist[u]])
    '''l = []
    for i in Wlist.keys():
        for (j, d) in Wlist[i]:
            l.append(d)
    inf = 1 + max(l)'''

    visited = {}
    distance = {}
    TreeEdges = []
    for i in Wlist.keys():
        distance[i] = inf
        visited[i] = False

    visited[0] = True   #random edge
    for (v,d) in Wlist[0]:
        distance[v] = d
        
    for i in Wlist.keys():
        min_dist = inf
        next_vert = None
        for j in Wlist.keys():
            for (k,d) in Wlist[j]:
                if visited[j]==True and visited[k]==False and d<min_dist:
                    min_dist = d
                    next_vert = v
                    next_edg = (u,v)

        if next_vert is None:
            break
        visited[next_vert] = True
        TreeEdges.append(next_edg)
        for (v, d) in Wlist[next_vert]:
            if visited[v] == False:
                distance[v] = min(distance[v], d)

    return TreeEdges

def prims2(Wlist):
    inf = 1 + max([d for u in Wlist.keys()
                       for (v,d) in Wlist[u]])
    visited = {}
    distance = {}
    neighbour = {}
    for i in Wlist.keys():
        distance[i] = inf
        visited[i] = False
        neighbour[i] = -1

    visited[0] = True   #random edge
    for (v,d) in Wlist[0]:
        distance[v] = d
        neighbour[v] = 0

    for i in range(1, len(Wlist.keys())):
        next_dist = min([distance[v] for v in Wlist.keys()
                             if not visited[v]])
        next_vert_list = [v for v in Wlist.keys()
                              if visited[v] == False and
                                  distance[v] == next_dist]
        if next_vert_list == []:
            break
        next_vert = min(next_vert_list)
        visited[next_vert] = True
        for (v, d) in Wlist[next_vert]:
            if visited[v] == False:
                distance[v] = min(distance[v], d)
                neighbour[v] = next_vert

    return neighbour
