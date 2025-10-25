def bellmanford(Wmat, s):
    (rows, cols, x) = Wmat.shape
    inf = np.max(Wmat)*rows + 1
    distance = {}
    for i in range(rows):
        distance[i] = inf
    distance[s] = 0

    for i in range(rows):
        for j in range(rows):
            for k in range(cols):
                if Wmat[j, k, 0] == 1:
                    distance[k] = min(distance[k], distance[j]+Wmat[j, k, 1])

    return distance
