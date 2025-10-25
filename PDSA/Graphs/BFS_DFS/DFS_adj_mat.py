(visited, parent) = ({}, {})

def DFS_init(a_mat):
    (rows, cols) = a_mat.shape
    (visited, parent) = ({}, {})
    for i in range(rows):
        visited[i] = False
        parent[i] = -1

def DFS(a_mat, v):
    visisted[v] = True

    for k in neighbours(a_mat, v):
        if (visited[k] == False):
            parent[k] = v
            DFS(a_mat, k)
