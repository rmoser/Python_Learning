# Advent of Code
year = 2016
day = 16

import numpy as np
import aocd

text0 = """
111100001010
"""
text1 = aocd.get_data(day=day, year=year)


def extend(text):
    a = text
    b = a[::-1].translate({48: 49, 49: 48})
    return f"{a}0{b}"


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    n = 272

    text = text1
    text = text.strip()

    while len(text) < n:
        text = extend(text)

    checksum = text[:n]
    while len(checksum) % 2 == 0:
        checksum = ''.join(['1' if a == b else '0' for a, b in zip(checksum[::2], checksum[1::2])])

    pone = checksum

    print(f"AOC {year} day {day}  Part One: {pone}")

    n = 35651584

    while len(text) < n:
        text = extend(text)

    checksum = text[:n]
    while len(checksum) % 2 == 0:
        checksum = ''.join(['1' if a == b else '0' for a, b in zip(checksum[::2], checksum[1::2])])

    ptwo = checksum

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
