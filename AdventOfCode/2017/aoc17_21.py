# Advent of Code
year = 2017
day = 21

import numpy as np
import aocd

text0 = """
../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#
"""
text1 = aocd.get_data(day=day, year=year)


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip()
    if '\n' in text:
        text = text.splitlines()

    rules = dict()
    for line in text:
        a, b = line.split(' => ')
        a = (np.array([list(s) for s in a.split('/')]) == '#').astype(int).astype(str)
        b = (np.array([list(s) for s in b.split('/')]) == '#').astype(int)
        for i in range(4):
            rules[''.join(a.flatten())] = b
            rules[''.join(a[::-1].flatten())] = b
            a = np.rot90(a)

    arr = (np.array([list(s) for s in """.#./..#/###""".split("/")], dtype=str) == '#').astype(int)

    for c in range(18):
        if c == 5:
            pone = arr.sum()

        print(f'\n{c}\n', arr)
        d = arr.shape[0]
        if d % 2 == 0:
            new = np.zeros((d // 2 * 3, d // 2 * 3), dtype=int)
            for i in range(d // 2):
                for j in range(d // 2):
                    _arr = arr[i*2:i*2+2, j*2:j*2+2].astype(str)
                    _a = ''.join(_arr.flatten())
                    new[i*3:i*3+3, j*3:j*3+3] = rules[_a]
            arr = new
            continue
        elif d % 3 == 0:
            new = np.zeros((d // 3 * 4, d // 3 * 4), dtype=int)
            for i in range(d // 3):
                for j in range(d // 3):
                    _arr = arr[i*3:i*3+3, j*3:j*3+3].astype(str)
                    _a = ''.join(_arr.flatten())
                    new[i*4:i*4+4, j*4:j*4+4] = rules[_a]
            arr = new
            continue
        break

    ptwo = arr.sum()

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
