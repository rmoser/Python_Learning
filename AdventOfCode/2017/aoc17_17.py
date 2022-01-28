# Advent of Code
year = 2017
day = 17

import numpy as np
import aocd

text0 = """3"""
text1 = aocd.get_data(day=day, year=year)

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip()
    if '\n' in text:
        text = text.splitlines()

    step = int(text)
    arr = [0]
    pos = 0
    for i in range(1, 2018):
        pos = (pos + step) % len(arr)
        arr = arr[:pos+1] + [i] + arr[pos+1:]
        pos += 1
        # print(i, pos, arr)

    pone = arr[pos+1]

    # print(pos1)

    pos = 0
    for i in range(1, 50000000):
        pos = (pos + step) % i + 1
        if pos == 1:
            ptwo = i

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
