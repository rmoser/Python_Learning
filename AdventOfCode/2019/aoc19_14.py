# Advent of Code
year = 2019
day = 14

import numpy as np
import aocd

text0 = """
10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL
"""
text1 = aocd.get_data(day=day, year=year)


class recipe(object):
    def __init__(self, name, ingredients):
        self.name = name

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text0
    text = text.strip()
    if '\n' in text:
        text = text.splitlines()


    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
