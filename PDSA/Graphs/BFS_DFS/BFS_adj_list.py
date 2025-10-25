def BFS(a_list, v):
    (level, parent) = ({}, {})      #level is shortest path based on number of nodes
    for i in a_list.keys():
        level[i] = -1
        parent[i] = -1

    q = Queue()     #write own class

    level[v] = 0
    q.addq(v)

    while (q.isempty() == False):
        j = q.delq()
        for k in a_list[j]:
            if (level[k] == -1):
                level[k] = level[j] + 1
                parent[k] = j
                q.addq(k)

    return (level, parent)

# if level [i] is -1, it is unreachable, otherwise it is the shortest distance (node wise) to that vertex
# you can backtrack up the parent dictionary of a node to find the shortest path to that vertex from v.
