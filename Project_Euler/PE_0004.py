# Project Euler p 4


def multmat(n):
    mat = [0] * (n)
    for i in range(n):
        mat[i] = [0]*n

    for x in range(n):
        for y in range(n - x):
            mat[y][x] = (x+1)*(y+1)

    print(mat)

def ispal(n):
    s = str(n)
    m = len(s)//2
    #print(n, m, s[:m], s[:-m-1:-1])
    return s[:m] == s[:-m-1:-1]


print(ispal(123))
print(ispal(2112))
print(ispal(21512))

def find_pal(n):
    ans = 1
    for x in range(n, 0, -1):
        for y in range(n, 0, -1):
            p = x * y
            if p > ans and ispal(p):
                ans = p
    return ans

print(find_pal(999))
