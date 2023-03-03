# Advent of Code
year = 2022
day = 12

import numpy as np
import aocd
import itertools

text0 = """
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""
text1 = aocd.get_data(day=day, year=year)


def show(arr, p=None, s=None, e=None):
    for r in range(arr.shape[0]):
        for c in range(arr.shape[1]):
            pos = (r, c)
            if pos == p:
                print('X', end='')
            elif pos == s:
                print('S', end='')
            elif isinstance(e, tuple) and pos == e:
                print('E', end='')
            else:
                print(chr(arr[(r, c)] + 97), end='')
        print('')


def path_step(arr, start, end, paths=None, up=True):
    moves = np.array([[1, 0], [-1, 0], [0, 1], [0, -1]])
    if not paths:
        paths = [[start]]
    coords = set((c for path in paths for c in path))
    for _ in range(len(paths)):
        path = paths.pop(0)
        pos = path[-1]

        new = moves + pos

        # Remove coordinates off the map
        valid = np.bitwise_and((new >= [0, 0]).all(axis=1), (new < arr.shape).all(axis=1))
        new = new[valid]

        # Remove invalid moves based on direction of travel
        if up:
            valid = (arr[tuple(new.T)] - arr[pos]) <= 1
        else:
            valid = (arr[tuple(new.T)] - arr[pos]) >= -1
        new = new[valid]

        # Remove moves that return to a point already visited by any path
        valid = [tuple(c) not in coords for c in new]
        new = new[valid]

        if isinstance(end, tuple):
            solution = (new == end).all(axis=1)
        else:
            solution = (arr[tuple(new.T)] == end)
        if solution.any():
            new = new[solution]

        for p in new:
            paths.append(path + [tuple(p)])
            coords.add(tuple(p))

    return paths


def find_path(arr, start, end, up=True):
    paths = None
    while True:
        paths = path_step(arr, start, end, paths, up=up)
        for path in paths:
            pos = path[-1]
            if (isinstance(end, tuple) and pos == end) or (isinstance(end, int) and arr[pos] == end):
                return [path]


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()
    shape = len(text), len(text[0])

    text = [ord(c) - 97 for x in text for c in x]
    arr = np.array(text).reshape(shape)

    start = tuple(np.argwhere(arr == -14)[0])
    end = tuple(np.argwhere(arr == -28)[0])

    pos = start
    arr[start] = 0
    arr[end] = 25

    paths = find_path(arr, start, end)

    pone = len(paths[0]) - 1

    # show(arr, pos, start, end)

    start_ptwo = end
    end_ptwo = 0

    paths = find_path(arr, start_ptwo, end_ptwo, up=False)
    ptwo = len(paths[0]) - 1

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
