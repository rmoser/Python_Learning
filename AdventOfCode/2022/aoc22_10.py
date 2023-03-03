# Advent of Code
year = 2022
day = 10

import numpy as np
import aocd

text0 = """
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
"""
#
# text0 = """
# noop
# addx 3
# addx -5
# """
text1 = aocd.get_data(day=day, year=year)

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    idx = [20, 60, 100, 140, 180, 220]

    display = np.zeros(shape=(6, 40), dtype=bool)
    reg = 1
    cycle = 0
    data = [1]
    for cmd in text:
        cmd = cmd.split()
        cycle += 1
        data.append(reg)
        if cmd[0] == 'addx':
            cycle += 1
            reg += int(cmd[1])
            data.append(reg)

    vals = [data[x-1] for x in idx]
    scores = [x * data[x-1] for x in idx]

    print(vals)
    print(scores)

    pone = sum(scores)
    print(f"AOC {year} day {day}  Part One: {pone}")

    for i in range(1, 241):
        draw_r = (i-1) // 40
        draw_c = (i-1) % 40

        # if draw_r > 5 or draw_c > 39:
        #     print(i, draw_r, draw_c)
        #     exit()

        # sprite_r = data[i] // 40
        sprite_c = data[i-1] % 40

        if abs(sprite_c - draw_c) <= 1:
            display[draw_r, draw_c] = True

    chars = [' ', '#']
    for r in range(display.shape[0]):
        for i in display[r]:
            print(chars[int(i)], end='')
        print('')

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
