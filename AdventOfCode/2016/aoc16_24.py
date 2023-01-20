# Advent of Code
year = 2016
day = 24

import numpy as np
import aocd
import utils
import itertools

text0 = """
###########
#0.1.....2#
#.#######.#
#4.......3#
###########
"""
text1 = aocd.get_data(day=day, year=year)

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    arr = utils.map_from_text(text)
    maze = arr == '#'
    utils.show(maze)

    pos = dict()
    for i in range(arr.shape[0] * arr.shape[1]):
        p = tuple(x[0] for x in np.where(arr == str(i)) if len(x))
        if not p:
            break
        pos[i] = p

    dist = dict()
    for i, (a, b) in enumerate(itertools.combinations(pos.keys(), r=2)):
        path = utils.valid_path(maze, start=pos[a], end=pos[b])
        dist[(a, b)] = len(path)-1
        dist[(b, a)] = len(path)-1

    paths = dict()
    for path in itertools.permutations(set(pos.keys()) - {0}, r=len(pos)-1):
        path = (0, *path)  # Always start at 0

        paths[path] = sum(dist[(a, b)] for a, b in zip(path[:-1], path[1:]))

    arr_paths = np.array(list(paths.keys()))
    arr_dists = np.array(list(paths.values()))

    pone = arr_dists.min()

    print(f"AOC {year} day {day}  Part One: {pone}")


    paths = dict()
    for path in itertools.permutations(set(pos.keys()) - {0}, r=len(pos)-1):
        path = (0, *path, 0)  # Always start at 0

        paths[path] = sum(dist[(a, b)] for a, b in zip(path[:-1], path[1:]))

    arr_paths = np.array(list(paths.keys()))
    arr_dists = np.array(list(paths.values()))

    ptwo = arr_dists.min()

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
