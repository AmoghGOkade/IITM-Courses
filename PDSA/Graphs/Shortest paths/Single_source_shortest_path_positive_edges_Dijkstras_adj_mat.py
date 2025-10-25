def dijkstra(Wmat, s):
    (rows, cols, x) = Wmat.shape    #x is 2 (tuple length)
    inf = np.max(Wmat)*rows + 1
    (visited, distance) = ({}, {})
    for i in range(rows):
        visited[i] = False
        distance[i] = inf

    distance[s] = 0     #start vertex
    for i in range(rows):
        next_dist = min([distance[j] for j in range(rows)
                             if not visited[j]])
        '''l =[]
        for j in range(rows):
            if visited[j] == False:
                l.append(distance[j])
        next_dist = min(l)'''

        next_vert_list = [j for j in range(rows)
                              if (not visited[j]) and
                                  distance[j] == next_dist]
        '''next_vert_list = []
        for j in range(rows):
            if (visited[j] == False and distance[j] == next_dist):
                next_vert_list.append(j)'''

        if next_vert_list == []:
            break

        next_vert = min(next_vert_list)
        visited[next_vert] = True
        for j in range(cols):
            if Wmat[next_vert, j, 0] == 1 and visited[j] == False:
                distance[j] = min(distance[j], distance[next_vert] + Wmat[next_vert, j, 1]

        return distance

# returns a dictionary having keys as the vertices and values as the shortest path from the start vertex based on weight.
