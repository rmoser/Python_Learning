# Advent of Code
year = 2019
day = 7

import numpy as np
import aocd
import itertools
from aoc19_05 import intcode

text0 = """3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0"""
text1 = aocd.get_data(day=day, year=year)

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip()
    if '\n' in text:
        text = text.splitlines()

    arr_init = [int(x) for x in text.split(',')]

    pone = 0
    phase = []
    for c in itertools.permutations(range(5)):
        val = 0
        for phase_value in c:
            val = intcode((phase_value, val), arr_init)
            # print(type(phase_value), val)
            val = val[-1]
        if val > pone:
            pone = val
            phase = c

    print(pone, phase)


    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
