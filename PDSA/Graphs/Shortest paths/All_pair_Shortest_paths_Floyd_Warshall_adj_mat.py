def floydwarshall(Wmat):
    (rows, cols, x) = Wmat.shape
    inf = np.max(Wmat)*rows + 1
    s_path = np.zeros(shape = (rows, cols, cols+1))     #3d array having a 3rd dimension for number of vertices you can use between 0 and k-1
    for i in range(rows):
        for j in range(cols):
            s_path[i, j, 0] = inf
    for i in range(rows):
        for j in range(cols):
            if Wmat[i, j, 0] == 1:
                s_path[i, j, 0] = Wmat[i, j, 1]     #SP^0 is the adj mat itself

    for k in range(1, cols+1):
        for i in range(rows):
            for j in range(cols):
                s_path[i, j, k] = min(s_path[i, j, k-1], s_path[i, k-1, k-1] + s_path[k-1, j, k-1])

    return s_path[:, :, cols]
