# Advent of Code
year = 2023
day = 11

import numpy as np
import aocd
import utils
import itertools

text0 = """
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""
text1 = aocd.get_data(day=day, year=year)

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()
    arr = (np.array([list(line) for line in text])=='#').astype(int)
    dist = np.ones(shape=arr.shape, dtype=np.int64)
    # print(arr)

    for r in range(arr.shape[0]-1, 0, -1):
        if arr[r,:].sum() == 0:
           dist[r,:] = 2

    for c in range(arr.shape[1]-1, 0, -1):
        if arr[:,c].sum() == 0:
            dist[:,c] = 2

    galaxies = [tuple(x) for x in np.asarray(np.where(arr==1)).T]
    distances = []
    for a, b in itertools.combinations(galaxies, 2):
        d = dist[min(a[0],b[0]):max(a[0],b[0]), a[1]].sum() + dist[b[0], min(a[1], b[1]):max(a[1],b[1])].sum()
        distances.append(d)
        # print(a, b, d)
    pone = np.sum(distances)

    dist[dist==2] = 1000000
    distances = []
    for a, b in itertools.combinations(galaxies, 2):
        d = dist[min(a[0],b[0]):max(a[0],b[0]), a[1]].sum() + dist[b[0], min(a[1], b[1]):max(a[1],b[1])].sum()
        distances.append(d)
        # print(a, b, d)
    ptwo = np.sum(distances)

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
