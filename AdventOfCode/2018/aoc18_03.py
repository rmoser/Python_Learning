# Advent of Code
year = 2018
day = 3

import numpy as np
import aocd

text0 = """
#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2
"""
text1 = aocd.get_data(day=day, year=year)

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip()
    if '\n' in text:
        text = text.splitlines()

    inst = []
    max_x = 0
    max_y = 0
    for line in text:
        i, line = line.split(" @ ")
        i = int(i[1:])
        c, line = line.split(": ")
        c = tuple(int(x) for x in c.split(","))
        a = tuple(int(x) for x in line.split("x"))
        max_x = max(max_x, c[0] + a[0] + 1)
        max_y = max(max_y, c[1] + a[1] + 1)
        inst.append((i, c, a))

    board = np.zeros(shape=(max_x, max_y, len(inst)+1), dtype=int)
    for box in inst:
        i, c, a = box
        end = tuple((c[0]+a[0], c[1]+a[1]))
        board[c[0]:end[0], c[1]:end[1], i] = 1
        # print(i, c, a, end)
        # print("\n", i)
        # print(board)

    count = board.sum(axis=2)

    pone = np.sum(count > 1)

    print(f"AOC {year} day {day}  Part One: {pone}")

    for i, c, a in inst:
        end = tuple((c[0]+a[0], c[1]+a[1]))
        if (count[c[0]:end[0], c[1]:end[1]] == 1).all():
            ptwo = i
            break

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
