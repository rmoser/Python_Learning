# Advent of Code
year = 2016
day = 5

import numpy as np
import aocd
import hashlib

text0 = """abc"""
text1 = aocd.get_data(day=day, year=year)


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1

    j = np.int64(0)
    pone = ''
    ptwo = list('........')

    while len(pone) < 8 or '.' in ptwo:
        s = f"{text}{j}".encode()
        h = hashlib.md5(s).hexdigest()
        if h[:5] == '00000':
            i, c = h[5:7]
            pone += i

            if i.isnumeric():
                i = int(i)
                if 0 <= i <= 7 and ptwo[i] == '.':
                    ptwo[i] = c

        if not j % 100:
            print(f"\rDecrypting: {''.join(ptwo)} cycle {j}", end='')

        j += 1

    print()
    ptwo = ''.join(ptwo)

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
