# Advent of Code
year = 2024
day = 20

import numpy as np
import aocd
import os
import utils
import itertools as it
from pprint import pprint
# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

text0 = """
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
"""
text1 = aocd.get_data(day=day, year=year)

def cheats(positions, time_limit):
    manhattan = np.full(shape=(len(positions), len(positions)), dtype=int, fill_value=len(positions)**2)
    time_delta = np.zeros_like(manhattan)

    result = dict()
    p = np.array(list(positions.keys()))
    v = np.array(list(positions.values()))

    for i in range(len(p)):
        manhattan[i] = np.abs(p[i] - p).sum(axis=1)
        time_delta[i] = v - v[i] - manhattan[i]

    time_delta *= time_delta > 0

    # print((manhattan == _manhattan).all())
    # print((time_delta[_time_delta>0] == _time_delta[_time_delta>0]).all())


    # gt = time_delta > 0
    # lt = time_delta < 0
    # time_delta[gt] -= manhattan[gt]
    # time_delta[lt] += manhattan[lt]

    for r in range(len(p)):
        row = manhattan[r]
        keep_indices = np.where(np.bitwise_and(manhattan[r] <= time_limit, time_delta[r] > 0))[0]
        for c in keep_indices:
            result[(tuple(p[r].tolist()), tuple(p[c].tolist()))] = time_delta[r, c]

    return result

    # DIRS = [c for c in it.combinations_with_replacement(np.arange(-20, 21), 2) if abs(np.array(c)).sum() <= time_limit]
    # result = dict()
    # for a in positions:
    #     for
    #     distance = np.abs(np.array(b) - a).sum()
    #     if distance <= time_limit:
    #         time_savings = positions[b] - positions[a]
    #         if time_savings > distance:
    #             result[(a, b)] = time_savings - distance
    #         elif time_savings < -distance:
    #             result[(b, a)] = -time_savings - distance
    # return result


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    if text == text0:
        threshold = 50
    else:
        threshold = 100

    text = text.strip().splitlines()
    array = np.array([list(line) for line in text])
    maze = (array == '#').astype(int)

    start = tuple(np.array(np.where(array == 'S')).transpose().flatten().tolist())
    end = tuple(np.array(np.where(array == 'E')).transpose().flatten().tolist())

    # utils.show(maze, start=start, end=end)

    print("Pathfinding...")
    x = utils.valid_path(maze, start, end)

    print("Scoring...")
    positions = dict(zip([(int(a[0]), int(a[1])) for a in x[0]], range(len(x[0]))))

    cheat_scores1 = cheats(positions, 2)
    cheat_scores2 = cheats(positions, 20)

    pone = sum(1 for x in cheat_scores1.values() if x >= 100)
    ptwo = sum(1 for x in cheat_scores2.values() if x >= 100)

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
