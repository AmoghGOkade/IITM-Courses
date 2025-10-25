def dijkstra(Wlist, s):
    inf = 1 + len(Wlist.keys()) * max([d for u in Wlist.keys()
                                           for (v,d) in Wlist[u]])
    '''l = []
    for i in Wlist.keys():
        for (v,d) in Wlist[i]:
            l.append(d)
    inf = 1 + len(Wlist.keys()) * max(l)'''

    visited = {}
    distance = {}

    for i in Wlist.keys():
        visited[i] = False
        distance[i] = inf
    distance[s] = 0

    for i in Wlist.keys():
        next_dist = min(distance[j] for j in Wlist.keys()
                            if not visited[j])
        '''l = []
        for j in Wlist.keys():
            if visited[j] == False:
                l.append(distance[j])
        next_dist = min(l)'''

        next_vert_list = [j for j in Wlist.keys()
                              if (not visited[j]) and
                                  distance[j] == next_dist]
        '''next_vert_list = []
        for j in Wlist.keys():
            if (visited[j] == False and distance[j] == next_dist):
                next_vert_list.append(j)'''

        if next_vert_list == []:
            break

        next_vert = min(next_vert_list)
        visited[next_vert] = True

        for (v,d) in Wlist[next_vert]:
            if visited[v] == False:     #does this line matter, its distance will anyways be lesser than the path throug this vertex if it was already visited
                distance[v] = min(distance[v], distance[next_vert] + d)

    return distance
