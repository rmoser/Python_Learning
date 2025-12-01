# Advent of Code
year = 2025
day = 1

import numpy as np
import aocd
import os
import utils
from pprint import pprint

text0 = """
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
"""
text1 = aocd.get_data(day=day, year=year)

debug = False


def dial(instructions, value=50):
    count = [0, 0]
    for instruction in instructions:
        if not instruction:
            continue
        if instruction[0] == "L":
            sign = -1
        else:
            sign = 1
        clicks = int(instruction[1:])

        if debug:
            print("\nins:", instruction, "val:", value, sign, "clicks:", clicks, "count:", count)

        count[1] += clicks // 100
        if clicks >= 100:
            if debug:
                print("full rotation:", count)
        clicks %= 100

        if debug:
            print("Checking for wraparound:\n", sign, "clicks:", clicks, "value:", value)
        if value and sign < 0 and clicks >= value:
            count[1] += 1
            if debug:
                print("left wrap:", count)
        elif value and sign > 0 and clicks + value >= 100:
            count[1] += 1
            if debug:
                print("right wrap:", count)

        value += sign * clicks
        value %= 100

        if value == 0:
            count[0] += 1

        if debug:
            print("End val:", value, "Count:", count)

    if debug:
        print()

    return count


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    pone, ptwo = dial(text)

    print(f"AOC {year} day {day}  Part One: {pone}")
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
