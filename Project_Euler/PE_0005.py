# Project Euler p 5

a = (10, 2520)
b = 20

def fact(n):
    d = {}
    v = n
    for i in range(2, int(n**0.5) + 1):
        d[i] = 0
        while v % i == 0:
            d[i] += 1
            v = v // i
    if v > 1:
        d[v] = 1
    return(d)

def maxfact(a,b):
    r = {}
    for k in a:
        r[k] = a[k]
    for k in b:
        if not k in r or a[k] < b[k]:
            r[k] = b[k]

    return(r)


def mult(d):
    a = 1
    for k in d:
        if d[k]:
            a *= k ** d[k]
    return(a)

print(fact(99))

x = {2:1, 6:1}
y = {2:4, 5:1}

print(maxfact(x,y))
print(mult(maxfact(x,y)))

print(fact(20))

def all(n):
    d = fact(n)
    for i in range(n):
        d = maxfact(d, fact(i))
    return mult(d)

print(all(10))
print(all(20))
