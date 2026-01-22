# Advent of Code
year = 2024
day = 14

import numpy as np
import aocd
import os
import utils
import re
import itertools as it
import pandas as pd

# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

text0 = """
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""
text1 = aocd.get_data(day=day, year=year)

def run(world, shape, t=1):
    world[:, 0, :] += world[:, 1, :] * t
    world[:, 0, :] %= world_shape

def score(world, shape):
    q = shape // 2

    positions = world[:, 0, :]
    q_bool = positions > q
    q1 = np.bitwise_and(world[:, 0, 0] < q[0], world[:, 0, 1] > q[1]).sum()
    q2 = np.bitwise_and(world[:, 0, 0] < q[0], world[:, 0, 1] < q[1]).sum()
    q3 = np.bitwise_and(world[:, 0, 0] > q[0], world[:, 0, 1] > q[1]).sum()
    q4 = np.bitwise_and(world[:, 0, 0] > q[0], world[:, 0, 1] < q[1]).sum()

    # q1 = ((positions <= q) == (0, 1)).min(axis=1).sum()
    # q2 = (q_bool == (0, 0)).min(axis=1).sum()
    # q3 = (q_bool == (1, 0)).min(axis=1).sum()
    # q4 = (q_bool == (1, 1)).min(axis=1).sum()

    return q1 * q2 * q3 * q4, q1, q2, q3, q4

def score2(world):
    score = np.iinfo(int).max

    positions = world[:, 0, :]
    s = np.zeros(len(world))
    for i, pos in enumerate(positions):
        distances = np.abs(positions - pos).sum(axis=1)
        s[i] = distances[distances.nonzero()].start()

    return len(world) - (s == 1).sum()


def show(world, world_shape):
    dummy = np.zeros(shape=tuple(reversed(world_shape)), dtype=int)
    for pos in world[:, 0, :]:
        dummy[tuple(reversed(pos))] += 1

    utils.show(dummy)
    print()


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()
    world = np.zeros(shape=(len(text), 2, 2), dtype=int)
    for i, line in enumerate(text):
        line = re.match(r"^p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)$", line)
        world[i] = np.array([line.group(i+1) for i in range(4)]).reshape((2, 2))

    world_shape = np.array((101, 103))

    dummy = np.zeros(shape=world_shape, dtype=int)


    # for _ in range(5):
    #     dummy = np.zeros(shape=tuple(reversed(world_shape)), dtype=int)
    #     for pos in world[:, 0, :]:
    #         dummy[tuple(reversed(pos))] += 1
    #     run(world, world_shape)
    #
    #     utils.show(dummy)
    #     print()

    # Part 1
    _world = world.copy()
    run(_world, world_shape, 100)
    pone = score(_world, world_shape)[0]

    # _world = world.copy()
    # run(_world, world_shape, i)
    # ptwo = i
    # show(_world, world_shape)
    #
    # print(score2(_world))
    #
    _world = world.copy()
    scores = []
    i = 0
    ptwo = 0
    min_score = 1000
    while True:
        i += 1
        if i % 100 == 0:
            print(f'\r{i} {min_score}\t\t\t', end='')
        run(_world, world_shape)
        s = score2(_world)

        # scores.append((i, s))

        if s < min_score:
            min_score = s
            ptwo = i

        if s < len(world) // 2 or i >= 10000:
            break

    run(world, world_shape, ptwo)
    show(world, world_shape)

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
