def longest_path(a_list):
    (indegree, lpath) = ({}, {})
    for u in a_list.keys():
        (indegree[u], lpath[u]) = (0,0)
    for u in a_list.keys():
        for v in a_list[u]:
            indegree[v] += 1

    zero_deg_q = Queue()
    for u in a_list.keys():
        if indegree[u] == 0:
            zero_deg_q.addq(u)

    while (zero_deg_q.isempty() == False):
        j = zero_deg_q.delq()

        indegree[j] -= 1
        for k in a_list[j]:
            indegree[k] -= 1
            lpath[k] = max(lpath[k], lpath[j]+1)
            if indegree[k] == 0:
                zero_deg_q.addq(k)

    return lpath
