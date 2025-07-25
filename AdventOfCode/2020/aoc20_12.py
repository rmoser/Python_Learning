# Advent of Code
year = 2020
day = 12

import numpy as np
import aocd
import os
from pprint import pprint
import itertools as it
import utils

# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

text0 = """
F10
N3
F7
R90
F11
"""
text1 = aocd.get_data(day=day, year=year)

CARDINALS = {'N': np.array([-1, 0]), 'E': np.array([0, 1]), 'S': np.array([1, 0]), 'W': np.array([0, -1])}
DIRECTIONS = (np.array([0, 1]), np.array([1, 0]), np.array([0, -1]), np.array([-1, 0]))

def run_one(text):
    pos = np.array((0, 0))
    direction = 0

    for line in text:
        inst = line[0]
        dist = int(line[1:])

        match inst:
            case 'F':
                d = DIRECTIONS[direction]
                pos = pos + d  * dist
            case 'N' | 'S' | 'E' | 'W':
                pos = pos + CARDINALS[inst] * dist
            case 'L':
                direction = (direction - dist // 90) % 4
            case 'R':
                direction = (direction + dist // 90) % 4

    return pos


def run_two(text):
    pos = np.array((0, 0))
    way = np.array((-1, 10))
    direction = 0

    for line in text:
        inst = line[0]
        dist = int(line[1:])

        match inst:
            case 'F':
                pos = pos + way * dist
            case 'N' | 'S' | 'E' | 'W':
                way = way + CARDINALS[inst] * dist
            case 'L' | 'R':
                dist = (dist // 90) % 4
                if dist == 1:
                    if inst == 'L':
                        way = np.array([-way[1], way[0]])
                    else:
                        way = np.array([way[1], -way[0]])

                elif dist == 2:
                    way = -way

                elif dist == 3:
                    if inst == 'L':
                        way = np.array([way[1], -way[0]])
                    else:
                        way = np.array([-way[1], way[0]])


        # print(line, pos, way)
    return pos


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    pone = np.abs(run_one(text)).sum()
    print(f"AOC {year} day {day}  Part One: {pone}")

    ptwo = np.abs(run_two(text)).sum()
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
