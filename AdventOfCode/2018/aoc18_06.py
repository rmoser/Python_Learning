# Advent of Code
year = 2018
day = 6

import numpy as np
import aocd
import itertools

text0 = """
1, 1
1, 6
8, 3
3, 4
5, 5
8, 9
"""
text1 = aocd.get_data(day=day, year=year)

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip()
    if '\n' in text:
        text = text.splitlines()

    coords = list()
    for coord in text:
        x, y = [int(x) for x in coord.split(', ')]
        coords.append(np.array((x, y)))

    coords = np.stack(coords)
    d = dict()
    for i, c in enumerate(coords):
        d[tuple(c)] = i
        d[i] = tuple(c)

    arr = np.full(fill_value=-1, shape=coords.max(axis=0)+2, dtype=int)
    arr2 = np.zeros(shape=arr.shape, dtype=int)
    for c in itertools.product(range(arr.shape[0]), range(arr.shape[1])):
        # print(c)
        delta = np.abs((coords - c))
        dists = delta.sum(axis=1)
        nearest = tuple(coords[dists.argmin()])
        n = d[nearest]
        if nearest == tuple(c):
            arr[c] = n
            # print(n)
        else:
            arr[c] = n
            # print(n)
        arr2[c] = dists.sum()

    outer = set(arr[0, :]) | set(arr[-1, :]) | set(arr[:, 0]) | set(arr[:, -1])

    inner = set(x for x in d.keys() if isinstance(x, int)) - outer

    areas = dict()
    for c in inner:
        areas[(arr == c).sum()] = c

    pone = max(areas)
    # pone = areas[k] - 1

    print(f"AOC {year} day {day}  Part One: {pone}")

    ptwo = (arr2 < 10000).sum()
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
