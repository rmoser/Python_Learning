def debt(balance, rate, payment):
    monthly = rate / 12.0
    b = balance

    for m in range(1, 13):
        b *= (1 - payment) * (1 + monthly)

    return b


def payment(balance, rate):
    for p in range(10, balance, 10):
        b = balance
        for i in range(12):
            b = (b - p) * (1 + rate / 12.0)

        if b <= 0:
            return p

def payment2(balance, rate):
    inc = 0.0100
    r = rate / 12.0
    lo = balance / 12.0
    hi = lo * (1 + r) ** 12.0

    while True:
        # Guess payment as midpoint of hi, lo
        p = round((hi + lo) / 2.0, 2)
        if isEnough(balance, rate, p):
            hi = p
        else:
            lo = p

        if hi - lo <= inc:
            return hi



def isEnough(balance, rate, p):
    for i in range(12):
        balance = (balance-p) * (1 + rate / 12.0)
        # print(i, balance)
    return balance <= 0


print(payment2(320000, 0.2))
print(payment2(999999, 0.18))

