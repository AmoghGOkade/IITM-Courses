def BFS(a_mat, v):      #the vertex whose reachable neighbours we want to find
    (rows, cols) = a_mat.shape      #no. of rows and columns
    visited = {}
    for i in range(rows):
        visited[i] = False

    q = Queue()     #make your own class

    visited[v] = True
    q.addq(v)

    while (q.isempty() == False):
        j = q.delq()
        for k in neighbours(a_mat, j):      #write a function to check whether a_mat[i][j] is 1 and return a list of all i's
            if (visited[k] == False):
                visited[k] = True
                q.addq(k)

    return visited

#visited has true if it is reachable and false otherwise
