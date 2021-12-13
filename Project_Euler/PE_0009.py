# Project Euler p 9

def pytho(n):
    for a in range(1, n-1):
        for b in range(a+1, n):
            c = n - a - b
            # print(a,b,c)
            if a ** 2 + b ** 2 == c ** 2:
                return a, b, c


print(pytho(30))
x = pytho(1000)

print(x)
print(x[0]*x[1]*x[2])
