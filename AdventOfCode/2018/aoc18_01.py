# Advent of Code
year = 2018
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
    text = text.strip()
    if '\n' in text:
        text = text.splitlines()
    text = [int(x) for x in text]

    pone = sum(text)

    print(f"AOC {year} day {day}  Part One: {pone}")


    d = dict()
    i = 0
    f = 0
    while True:
        f += text[i]
        if f in d:
            ptwo = f
            break
        d[f] = 0
        i += 1
        if i == len(text):
            i = 0


    print(f"AOC {year} day {day}  Part Two: {ptwo}")
