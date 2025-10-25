def fib(n):
    if n in fibtable.keys():
        return fibtable[n]
    if n <= 1:
        value = n
    else:
        value = fib(n-1) + fib(n-2)
    fibtable[n] = value
    return value

fibtable = {}
