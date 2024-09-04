# Advent of Code
year = 2023
day = 16

import numpy as np
import aocd
import os
# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
import utils

text0 = r"""
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
"""
text1 = aocd.get_data(day=day, year=year)

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = [list(c) for c in text.strip().splitlines()]
    arr = np.array(text)

    dirs = np.array([[0, 1], [1, 0], [0, -1], [-1, 0]])
    beams = [[(0, 0), 0]]
    direction = 0
    energized = set()

    history = np.zeros(arr.shape + (4, ), dtype=bool)

    counter = 0
    while(beams):
        # counter += 1
        # if counter == 1000:
        #     break

        pos, direction = beams.pop(0)
        energized.add(pos)
        # print(pos, direction)
        if history[pos][direction]:
            continue
        history[pos][direction] = True

        if arr[pos] == '.':
            pass

        elif arr[pos] == '|' and direction in (0, 2) or arr[pos] == '-' and direction in (1, 3):
            beams.append([pos, (direction+1) % 4])
            beams.append([pos, (direction+3) % 4])

            # print('split', beams, energized)
            # if arr[pos] == '-':
            #     counter = 990
            continue

        elif arr[pos] == '\\':
            if direction in (0, 1):
                direction = 1 - direction
            else:
                direction = 5 - direction
        elif arr[pos] == '/':
            direction = 3 - direction

        pos = tuple((pos + dirs[direction]).tolist())

        if 0 <= pos[0] < arr.shape[0] and 0 <= pos[1] < arr.shape[1]:
            beams.append([pos, direction])

        # print(len(beams))

    pone = len(energized)

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
