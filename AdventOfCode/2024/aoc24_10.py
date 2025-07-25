# Advent of Code
year = 2024
day = 10

import numpy as np
import aocd
import os
import utils
# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

text0 = """
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""
text1 = aocd.get_data(day=day, year=year)

DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def walk(paths, arr):
    if all(isinstance(x, int) for x in paths):
        paths = [[paths]]

    done = []
    while paths:
        path = paths.pop(0)
        pos = path[-1]
        for dir in DIRS:
            new_pos = pos + np.array(dir)
            # print(pos, new_pos)
            if (new_pos >= 0).all() and (new_pos < arr.shape).all():
                new_pos = tuple(new_pos.tolist())
                if arr[new_pos] == (arr[pos] + 1) and new_pos not in path:
                    # print(len(paths), pos, new_pos)
                    _path = path + [new_pos]
                    if arr[new_pos] == 9:
                        done.append(_path)
                    else:
                        # print("add path")
                        paths.append(_path)
                        # print(len(paths))
    return done

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()
    array = np.array([list(line) for line in text])
    # array[array == '.'] = '1'
    array = array.astype(int)

    # utils.show(array, translate=False)

    trailheads = [[tuple(x)] for x in np.array(np.where(array == 0)).transpose().tolist()]

    paths = walk(trailheads, array)

    # print(paths)

    d = dict()
    for path in paths:
        if path[0] not in d:
            d[path[0]] = set()
        d[path[0]].add(path[-1])

    # for p in paths:
    #     utils.show(array, path=p, translate=False)

    pone = sum(len(s) for s in d.values())
    ptwo = len(paths)

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
