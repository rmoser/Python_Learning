# Project Euler p 10

def primes(n, idx=0):
    prime_list = []
    window = 10000
    intervals = range(2, int(n+1), min(n, window))

    for i in intervals:
        arr = range(i, i+window)
        end = max(arr)
        #print(i, max(arr), len(prime_list))
        d = {}
        for v in arr:
            d[v] = True

        for v in arr:
            if not(d[v]):
                continue

            for p in prime_list:
                if v % p == 0:
                    d[v] = False
                    for inv in range(v, end, p):
                        d[v] = False
                    continue
            if d[v]:
                prime_list.append(v)

        if 0 < len(prime_list) <= idx:
            return (prime_list[idx - 1], prime_list)

        print(i, len(prime_list))

    return(prime_list)

#print(primes(10, 0))

n = 10

n = 2000000
print(sum([x for x in primes(n) if x < n]))

# This is slow, so the result is: 142913828922
