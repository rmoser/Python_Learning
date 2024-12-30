# Advent of Code
year = 2024
day = 6

import numpy as np
import aocd
import os
import utils
from enum import Enum

# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

text0 = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""
text1 = aocd.get_data(day=day, year=year)

DIRS = tuple(np.array(x) for x in ((-1, 0), (0, 1), (1, 0), (0, -1)))
global ARRAY
ARRAY = None

RETURN_CODES = Enum('Return Code', [('PASS', 0), ('EXIT', 1), ('LOOP', 2)])

def in_array(pos):
    _pos = np.array(pos)
    return np.all(_pos >= 0) and np.all(_pos < ARRAY.shape)

def walk(pos, direction, array=None):
    if array is None:
        array = ARRAY
    guard_path = []

    _path = set()

    while True:
        if (pos, direction) in guard_path:
            return guard_path, RETURN_CODES['LOOP']
        guard_path.append((pos, direction))
        _path.add(pos)

        _pos = tuple((pos + DIRS[direction]).tolist())

        if not in_array(_pos):
            return guard_path, RETURN_CODES['EXIT']

        while array[_pos] == '#':
            direction = (direction + 1) % 4
            guard_path.append((pos, direction))
            _pos = tuple((pos + DIRS[direction]).tolist())

        # Update position and continue walk
        pos = _pos

        # print("\r", len(_path), pos, end='               ')


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    ARRAY = np.array([list(line) for line in text])
    if False:
        ARRAY[(112, 50)] = '#'

    start = tuple(np.array(np.where(ARRAY == '^')).flatten().tolist())
    pos = start
    direction = 0

    obstacles = []

    guard_path, return_code = walk(pos, direction)

    positions = [p for p, _ in guard_path]

    pone = len(set([p for p, _ in guard_path]))

    print(f"AOC {year} day {day}  Part One: {pone}")

    if True:
        _path = set(x[0] for x in guard_path[1:])
        for i, p in enumerate(_path):
            print('\r', i, len(_path), p, end='                    ')
            print('\r                   ', end='\r')
            array = ARRAY.copy()
            array[p] = '#'
            _, return_code = walk(pos, direction, array)
            if return_code == RETURN_CODES['LOOP']:
                obstacles.append(p)

    ptwo = len(obstacles)

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
