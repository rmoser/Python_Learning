# Advent of Code
year = 2015
day = 3

import numpy as np
import aocd

text0 = "^>v<"
text1 = aocd.get_data(day=day, year=year)


if __name__ == '__main__':
    text = text1

    y_dim = 1 + sum(c in "^v" for c in text)
    x_dim = 1 + sum(c in "<>" for c in text)

    mat1 = np.zeros((x_dim, y_dim), int)

    y_start = sum(c == "v" for c in text)
    x_start = sum(c == "<" for c in text)

    print(x_start, y_start)
    print(x_dim, y_dim)

    start = (x_start, y_start)
    mat1[start] = 1
    mat2 = mat1.copy()

    santa_solo = start

    santa = start
    robot = start

    def update_pos(pos, c):
        if c == "<":
            pos = (pos[0] - 1, pos[1])
        elif c == ">":
            pos = (pos[0] + 1, pos[1])
        elif c == "v":
            pos = (pos[0], pos[1] - 1)
        elif c == "^":
            pos = (pos[0], pos[1] + 1)

        return pos

    for s, r in zip(text[::2], text[1::2]):
        santa_solo = update_pos(santa_solo, s)
        mat1[santa_solo] += 1
        santa_solo = update_pos(santa_solo, r)
        mat1[santa_solo] += 1

        santa = update_pos(santa, s)
        mat2[santa] += 1
        robot = update_pos(robot, r)
        mat2[robot] += 1

    print(f"AOC {year} day {day}  Part One: {(mat1 > 0).sum()}")

    print(f"AOC {year} day {day}  Part Two: {(mat2 > 0).sum()}")
