# Advent of Code
year = 2016
day = 9

import numpy as np
import aocd

text0 = """
ADVENT
A(1x5)BC
(3x3)XYZ
A(2x2)BCD(2x2)EFG
(6x1)(1x3)A
X(8x2)(3x3)ABCY
"""
text1 = aocd.get_data(day=day, year=year)


def my_len(s):
    total = 0
    i = 0
    start = 0
    while i < len(s):
        c = s[i]

        if c == '(':
            start = i+1
            i += 1
            continue

        if c == ')':
            cmd = tuple(int(x) for x in s[start:i].split('x'))
            sub = s[i+1:i+1+cmd[0]]
            # print(cmd, sub)
            total += cmd[1] * my_len(sub)
            # s += sub * cmd[1]
            i += 1 + cmd[0]
            start = 0
            continue

        if not start:
            total += 1

        i += 1

    return total


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    pone = 0
    ptwo = 0
    for line in text:
        print(line)
        ptwo += my_len(line)
        s = ''
        i = 0
        start = 0
        while i < len(line):
            c = line[i]

            if c == '(':
                start = i+1
                i += 1
                continue

            if c == ')':
                cmd = tuple(int(x) for x in line[start:i].split('x'))
                sub = line[i+1:i+1+cmd[0]]
                # print(cmd, sub)
                s += sub * cmd[1]
                i += 1 + cmd[0]
                start = 0
                continue

            if not start:
                s += c

            i += 1

        # print(len(s), s)
        # print()
        pone += len(s)

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
