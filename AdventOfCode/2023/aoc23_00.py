# Advent of Code
year = 2023
day = 0

import numpy as np
import aocd
import os
import utils
from pprint import pprint
import itertools as it
import math

text0 = """
"""
text1 = aocd.get_data(day=day, year=year)

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text0
    text = text.strip().split('\n\n' if '\n\n' in text else '\n')


    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
