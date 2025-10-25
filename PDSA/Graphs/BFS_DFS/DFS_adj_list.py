(visited, parent) = ({}, {})

def DFS_init(a_list):
    for i in a_list.keys():
        visited[i] = False
        parent[i] = -1

def DFS(a_list, v):
    visited[v] = True

    for k in a_list[v]:
        if visited[k] == False:
            parent[k] = v
            DFS(a_list, k)
