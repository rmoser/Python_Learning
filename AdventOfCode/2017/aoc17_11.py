# Advent of Code
year = 2017
day = 11

import numpy as np
import aocd

text0 = """
ne,ne,ne
ne,ne,sw,sw
ne,ne,s,s
se,sw,se,sw,sw
"""
text1 = aocd.get_data(day=day, year=year)

d = {'n': (0., 1.),
     's': (0., -1.),
     'ne': (1., 0.5),
     'se': (1., -0.5),
     'nw': (-1., 0.5),
     'sw': (-1., -0.5)
     }


def dist(steps):
    max_d = 0
    pos = np.array([0, 0], dtype=float)
    for step in steps.split(','):
        pos += d[step]

        a_pos = np.abs(pos)
        max_d = max(max_d, int(a_pos[1] + a_pos[0] / 2) if a_pos[0] <= 2 * a_pos[1] else int(pos[0]))

    print(pos)
    a_pos = np.abs(pos)
    result = int(a_pos[1] + a_pos[0] / 2) if a_pos[0] <= 2 * a_pos[1] else int(pos[0])

    return result, max_d
    # return tuple(pos)


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = list(text.strip().splitlines())

    # for line in text:
    #     print(line, dist(line))

    pone, ptwo = dist(text[0])

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
