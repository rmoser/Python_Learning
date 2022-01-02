# Advent of Code
year = 2016
day = 1

import numpy as np
import aocd

text0 = """ 
"""
text1 = aocd.get_data(day=day, year=year)


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().split(', ')

    def move(orientation, dist, pos, locs):
        global ptwo
        for _ in range(dist):
            if orientation == 0:
                pos[1] += 1
            elif orientation == 180:
                pos[1] -= 1
            elif orientation == 90:
                pos[0] += 1
            else:
                pos[0] -= 1

            if not ptwo and tuple(pos) in locs:
                print(f"ptwo: {pos}")
                ptwo = np.abs(pos).sum()
            else:
                locs.add(tuple(pos))

        return orientation, pos, locs

    orientation = 0
    pos = [0, 0]

    locs = set()

    for cmd in text:
        direction = cmd[0]
        dist = int(cmd[1:])

        if direction == 'R':
            orientation += 90
        else:
            orientation -= 90
        orientation %= 360

        orientation, pos, locs = move(orientation, dist, pos, locs)

    pone = np.abs(pos).sum()

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
