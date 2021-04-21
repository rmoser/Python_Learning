# Project Euler p 7

def primes(n, idx=0):
    prime_list = []
    intervals = list(range(2, int(n+1), 100))

    for i in intervals:
        arr = range(i, i+100)
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
                    for inv in range(v, max(arr), p):
                        d[v] = False
                    continue
            if d[v]:
                prime_list.append(v)

        if 0 < len(prime_list) <= idx:
            return (prime_list[idx - 1], prime_list)

    return(prime_list)

#print(primes(200, 5))
print(primes(1000000, 10001))
