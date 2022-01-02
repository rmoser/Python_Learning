# Advent of Code
year = 2016
day = 2

import numpy as np
import aocd

text0 = """ 
ULL
RRDDD
LURDL
UUUUD
"""
text1 = aocd.get_data(day=day, year=year)


def key(pos):
    # pos is row, col
    return 1 + pos[0] * 3 + pos[1]


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    # pos is row, col
    pos = [1, 1]

    code = 0
    for line in text:
        for c in line:
            if c == 'U':
                pos[0] = max(0, pos[0] - 1)
            elif c == 'D':
                pos[0] = min(2, pos[0] + 1)
            elif c == 'R':
                pos[1] = min(2, pos[1] + 1)
            else:
                pos[1] = max(0, pos[1] - 1)
            # print(c, pos)

        code = code * 10 + key(pos)

    pone = code

    print(f"AOC {year} day {day}  Part One: {pone}")

    key2 = np.array([
        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', '1', ' ', ' ', ' '],
        [' ', ' ', '2', '3', '4', ' ', ' '],
        [' ', '5', '6', '7', '8', '9', ' '],
        [' ', ' ', 'A', 'B', 'C', ' ', ' '],
        [' ', ' ', ' ', 'D', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ']
    ])

    code2 = ''
    text = text1
    text = text.strip().splitlines()

    # pos is row, col
    pos = np.array([3, 1])

    for line in text:
        for c in line:
            if c == 'U':
                _pos = pos + (-1, 0)
            elif c == 'D':
                _pos = pos + (1, 0)
            elif c == 'R':
                _pos = pos + (0, 1)
            else:
                _pos = pos + (0, -1)

            if key2[tuple(_pos)] != ' ':
                pos = _pos

        code2 += key2[tuple(pos)]

    ptwo = code2

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
