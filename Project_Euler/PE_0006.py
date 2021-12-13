# Project Euler p 6
import numpy as np
a = 10
b = 100

def sum_of_sq(n):
    s = 0
    for i in range(n):
        s += (i+1)**2
    return(s)

def sum_nums(n):
    return(n * (n+1) // 2)

def show(n):
    a = sum_of_sq(n)
    b = sum_nums(n) ** 2
    print("")
    print(n, " sumsq: ", a)
    print(n, " sqsum: ", b)
    print(n, " diff: ", abs(a-b))


show(a)
show(b)

