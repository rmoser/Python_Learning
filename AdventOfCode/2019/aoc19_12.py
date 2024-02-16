# Advent of Code
year = 2019
day = 12

import numpy as np
import aocd
import itertools as it
import math

text0 = """
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>
"""

# text0 = """
# <x=-8, y=-10, z=0>
# <x=5, y=5, z=10>
# <x=2, y=-7, z=3>
# <x=9, y=-8, z=-3>
# """

text1 = aocd.get_data(day=day, year=year)


def energy(arr):
    return sum(np.abs(a[:3]).sum() * np.abs(a[3:]).sum() for a in arr)


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text0
    text = text.strip()
    if '\n' in text:
        text = text.splitlines()

    moons = []
    for line in text:
        moons.append(np.array([int(a.split('=')[1]) for a in line.strip("<>").split(', ')] + [0, 0, 0]))

    periods = [[None]*3, [None]*3, [None]*3, [None]*3]
    t = 0
    states = [[list(), list(), list()], [list(), list(), list()], [list(), list(), list()], [list(), list(), list()]]
    for i in range(4):
        states[i][0].append((moons[i][0], moons[i][3]))
        states[i][1].append((moons[i][1], moons[i][4]))
        states[i][2].append((moons[i][2], moons[i][5]))

    while not all((all(x) for x in periods)):
        t += 1
        if t == 1000:
            pone = energy(moons)

        # Update velocities
        for a, b in it.combinations(moons, 2):
            # print(a[0], b[0])
            delta_v = (a[:3] < b[:3]).astype(int) - (a[:3] > b[:3])
            a[3:] += delta_v
            b[3:] -= delta_v
            # print(delta_v)

        # Update positions
        for m in moons:
            m[:3] += m[3:]

        for i in range(4):
            state = tuple(moons[i])
            state_x = state[0], state[3]
            state_y = state[1], state[4]
            state_z = state[2], state[5]

            if not periods[i][0] and state_x in states[i][0]:
                periods[i][0] = t
            if not periods[i][1] and state_y in states[i][1]:
                periods[i][1] = t
            if not periods[i][2] and state_z in states[i][2]:
                periods[i][2] = t

            states[i][0].append(state_x)
            states[i][1].append(state_y)
            states[i][2].append(state_z)

        if t % 1000 == 0:
            print(f"{t}...")

        if t == 2772:
            break

    print(moons)
    print(periods)

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(periods)
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
