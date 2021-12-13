# Project Euler p3

# Largest prime factor

a = 600851475143

def reduce(n):
    v = n
    large = 1
    est = int(v ** 0.5)+1
    for i in range(2, est):
        while v % i == 0:
            large = i
            v = v // i

    return max(large, v)


def primes(n):
    ans = []
    arr = list(range(2, int(n+1), 1))

    while len(arr):
        x = arr.pop(0)
        ans.append(x)
        arr = [i for i in arr if i % x > 0]

    return(ans)

ans = reduce(a)
valid = ans in primes(ans)
print("ans: ", ans)
print("Valid: ", ans)

