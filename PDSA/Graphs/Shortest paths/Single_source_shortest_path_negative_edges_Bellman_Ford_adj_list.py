def bellmanford(Wlist, s):
    inf = 1 + len(Wlist.keys()) * max([d for u in Wlist.keys()
                                           for (v,d) in Wlist[u]])
    distance = {}
    for i in Wlist.keys():
        distance[i] = inf
    distance[s] = 0

    for i in Wlist.keys():      #running n times, but can run n-1 times also
        for j in Wlist.keys():
            for (k,d) in Wlist[j]:
                distance[k] = min(distance[k], distance[j] + d)

    return distance
