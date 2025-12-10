# Advent of Code

year = 2025
day = 10

import numpy as np
import aocd
import os
import utils
from pprint import pprint
from icecream import ic
import itertools as it

text0 = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
"""
text1 = aocd.get_data(day=day, year=year)

def solve(goal, buttons, joltage):
    for i in range(1, len(buttons)+1):
        for group in it.combinations(buttons, i):
            # ic(group)
            state = np.zeros_like(goal, dtype=bool)
            for button in group:
                state ^= button
            if (state == goal).all():
                return len(group), group
    return 0

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    machines = []
    for line in text:
        words = line.split()
        goal = np.array([0 if x == '.' else 1 for x in words[0][1:-1]], dtype=bool)
        buttons = [[int(y) for y in x[1:-1].split(',')] for x in words[1:-1]]
        buttons = [np.array([i in button for i in range(len(goal))]) for button in buttons]

        joltage = [int(x) for x in words[-1][1:-1].split(',')]

        ic(goal, buttons, joltage)

        machines.append([goal, buttons, joltage])

    # ic(solve(*machines[0]))
    pone = sum((solve(*machine)[0] for machine in machines))


    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
