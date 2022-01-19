# Advent of Code
year = 2017
day = 5

import numpy as np
import aocd

text0 = """
0
3
0
1
-3
"""
text1 = aocd.get_data(day=day, year=year)


def run(program, pone=True):
    i = 0
    c = 0
    while 0 <= i < len(program):
        j = program[i]
        # print(c, i, program, j)
        if pone or program[i] < 3:
            program[i] += 1
        else:
            program[i] -= 1
        i += j
        c += 1

    # print(program)

    return c


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()
    program = [int(c) for c in text]

    pone = run(program.copy())

    print(f"AOC {year} day {day}  Part One: {pone}")

    ptwo = run(program.copy(), pone=False)

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
