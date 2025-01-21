# Advent of Code
year = 2017
day = 1

import numpy as np
import aocd

text0 = """1122
1111
1234
91212129
"""
text1 = aocd.get_data(day=day, year=year)


def parse(line, n=1):
    return sum(int(a) if a == b else 0 for a, b in zip(line, line[n:] + line[:n]))


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    DEBUG = False

    text = text1
    text = text.strip().splitlines()

    for line in text:
        count = parse(line)
        if DEBUG:
            print(line, count)

    pone = count

    print(f"AOC {year} day {day}  Part One: {pone}")

    for line in text:
        count = parse(line, n=len(line)//2)
        if DEBUG:
            print(line, count)

    ptwo = count

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
