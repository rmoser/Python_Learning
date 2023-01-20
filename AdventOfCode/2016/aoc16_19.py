# Advent of Code
year = 2016
day = 19

import numpy as np
import aocd

text0 = "5"

text1 = aocd.get_data(day=day, year=year)


def play(n, pone=True):
    if pone:
        r = list(range(1, n+1))
        while len(r) > 1:
            # print(r)
            r_keep = []
            for i in range(0, len(r), 2):
                r_keep.append(r[i])
                if i == len(r)-1:
                    r_keep.pop(0)
            r = r_keep

        return r[0]

    print("Part Two:")
    # Part Two
    r = np.ma.arange(1, n+1)
    r.mask = [False] * r.count()
    rc = r.compressed()

    r_choose = r // 2

    debug = r.count() < 20

    j = 0
    while n > 1:
        print('len: ', r.count())
        for i in rc-1:
            j += 1
            if r.mask[i]:
                continue
            idx_self = (rc == r[i]).argmax()
            idx_other_rc = (idx_self + n // 2) % n
            idx_other = rc[idx_other_rc] - 1
            r.mask[idx_other] = True
            rc = r.compressed()
            n = r.count()

            if debug:
                print(f'\r{i} {r[i]} took {r.item(idx_other)}: {rc}', end='\n')
            elif j % 1000 == 0:
                print(f'\riter {i}', end='')

    print()
    print("Result: ", r.compressed())
    return r.compressed()[0]


def play2(n):
    import math
    debug = True
    r = list(range(1, n+1))
    i = 0
    r_len = n
    for _i in range(n-1):
        d = (i + r_len // 2) % r_len
        r.pop(d)
        r_len -= 1
        i += 1
        if i >= r_len:
            i = 0

        if debug or r_len % 10000 == 0:
            print(r_len, r)

    return r[0]


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = int(text.strip())

    pone = play(text, pone=True)

    print(f"AOC {year} day {day}  Part One: {pone}")

    ptwo = play2(text)

    print(f"AOC {year} day {day}  Part Two: {ptwo}")

