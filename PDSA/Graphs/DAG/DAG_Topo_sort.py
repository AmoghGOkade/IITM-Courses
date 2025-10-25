def toposort_mat(a_mat):
    (rows, cols) = a_mat.shape
    indegree = {}
    topo_sorted_list = []

    for c in range(cols):
        indegree[c] = 0
        for r in range(rows):
            if a_mat[r,c] == 1:
                indegree[c] = indegree[c] + 1

    for i in range(rows):
        j = min([k for k in range(cols)
                 if indegree[k] == 0])
        
        topo_sorted_list.append(j)
        indegree[j] -= 1        #to not check it again, we can do indegree[j] = -1 also

        for k in range(cols):
            if a_mat[j,k] == 1:
                indegree[k] -= 1

    return topo_sorted_list

def toposort_list_me(a_list):      #me
    topo_sorted_list = []
    
    indegree = {}
    for i in a_list.keys():
        indegree[i] = 0
    for i in a_list.keys():
        for j in a_list[j]:
            indegree[j] += 1

    for i in a_list.keys():
        for j in a_list.keys():
            if indegree[j] == 0:
                indegree[j] -= 1
                topo_sorted_list.append(j)
                for k in a_list[j]:
                    indegree[k] -= 1

    return topo_sorted_list

def toposort_list(a_list):      #pdsa video
    (indegree, topo_sorted_list) = ({}, [])
    for u in a_list.keys():
        indegree[u] = 0
    for u in a_list.keys():
        for v in a_list[u]:
            indegree[v] += 1

    zero_deg_q = Queue()        #write own class
    for u in a_list.keys():
        if indegree[u] == 0:
            sero_deg_q.addq(u)

    while (zero_deg_q.isempty() == False):
        j = zero_deg_q.delq()
        topo_sorted_list.append(j)
        indegree[j] -= 1

        for k in a_list[j]:
            indegree[k] -= 1
            if indegree[k] == 0:
                zero_deg_q.addq(k)

    return topo_sorted_list
