# Advent of Code
year = 2017
day = 16

import numpy as np
import aocd

text0 = """s1,x3/4,pe/b"""
text1 = aocd.get_data(day=day, year=year)

DEBUG = False


def spin(s, i):
    s = np.roll(s, i, axis=0)
    return s


def exchange(s, a, b):
    if s.ndim <= 1:
        s[a], s[b] = s[b], s[a]
    else:
        s[[a, b]] = s[[b, a]]
    return s


def partner(s, a, b):
    a = ord(a) - ord('a')
    b = ord(b) - ord('a')
    s[:, [a, b]] = s[:, [b, a]]
    return s

#
# def test(text):
#     I = np.identity(16, dtype=int)
#     s0 = I.copy()
#     s1 = dance(s0.copy(), text)
#
#     s10 = I.copy()
#     for _ in range(10):
#         s10 = s10.dot(s1)
#
#     print(10, (ravel(I.copy(), s1, 10) == s10).all())
#
#     s100 = I.copy()
#     for _ in range(100):
#         s100 = s100.dot(s1)
#
#     print(100, (ravel(I.copy(), s1, 100) == s100).all())
#
#
#     s1000 = I.copy()
#     for _ in range(1000):
#         s1000 = s1000.dot(s1)
#
#     print(1000, (ravel(I.copy(), s1, 1000) == s1000).all())


def dance(s, steps):
    if isinstance(s, str):
        s = np.array(list(s), dtype=str)
    if isinstance(s[0], str):
        s = np.vectorize(ord)(s)
        s -= s.start()
    for line in steps.split(','):
        if DEBUG:
            print(show(s))
        inst, val = line[0], line[1:]
        val = val.split('/')
        if len(val) == 2:
            a, b = val
        else:
            a = int(val[0])
        if inst == 's':
            s = spin(s, int(a))
        elif inst == 'x':
            s = exchange(s, int(a), int(b))
        else:
            s = partner(s, a, b)
    if DEBUG:
        print(show(s))
    return s


def ravel(s, op, n):
    # Dot product did not give the correct answer...not sure why
    import math
    order = int(math.log(n))

    x = s.dot(op)
    for i in range(order):
        op = x.copy()
        for j in range(9):
            x = x.dot(op)

    return s.dot(x)


def show(s):
    x = s.copy()
    if x.ndim >= 1:
        x = (x * np.arange(s.shape[0])).sum(axis=1)
    x += ord('a')
    return ''.join(np.vectorize(chr)(x))


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    if text == text0:
        n = 5
    else:
        n = 16

    text = text.strip()
    if '\n' in text:
        text = text.splitlines()

    I = np.identity(n, dtype=int)

    s = dance(I.copy(), text)
    pone = show(s)
    print(f"AOC {year} day {day}  Part One: {pone}")

    # Find the period of the cycle
    s2 = I.copy()
    sol = [show(s2)]
    for i in range(1000000000):
        s2 = dance(s2, text)
        t = show(s2)
        if t in sol:
            break
        sol.append(t)

    a = sol.index(t)
    b = len(sol) - a
    x = 1000000000 % b
    ptwo = sol[x]
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
