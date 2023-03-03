# Advent of Code
year = 2022
day = 9

import numpy as np
import aocd

text0 = """
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""

texta = """
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
"""

text1 = aocd.get_data(day=day, year=year)

moves = {
    'R': np.array([0, 1]),
    'L': np.array([0, -1]),
    'U': np.array([1, 0]),
    'D': np.array([-1, 0])
}


def move(a, b):
    delta = (a - b)
    if (np.abs(delta) > 1).any():
        b += np.sign(delta)
    return b


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    rope = np.zeros(shape=(10, 2), dtype=int)
    rope_hist = list()
    for i in range(10):
        rope_hist.append({(0, 0)})

    for c, cmd in enumerate(text):
        direction, dist = cmd.split()
        dist = int(dist)

        for i in range(dist):
            rope[0] += moves[direction]
            for i in range(9):
                t = move(rope[i], rope[i+1])
            # print(c, cmd, i, h, t)

            for i in range(10):
                rope_hist[i].add(tuple(rope[i]))

    pone = len(rope_hist[1])
    ptwo = len(rope_hist[9])

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
