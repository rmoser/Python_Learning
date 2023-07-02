# Advent of Code
year = 2019
day = 4

import numpy as np
import aocd

text0 = """
"""
text1 = aocd.get_data(day=day, year=year)


def check(n, mode=1):
    n_str = str(n)
    n_list = [int(x) for x in str(n)]
    n_list_z = list(zip(n_list[:-1], n_list[1:]))
    if any(a > b for a, b in n_list_z):
        return False
    if all(a != b for a, b in n_list_z):
        return False
    if mode == 1:
        return True

    if any(str(x)*2 in n_str and str(x)*3 not in n_str for x in range(1, 10)):
        return True
    else:
        return False


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip()
    if '\n' in text:
        text = text.splitlines()

    a, b = [int(x) for x in text.split('-')]

    r = range(a, b+1)

    pone = sum(check(x) for x in r)

    print(f"AOC {year} day {day}  Part One: {pone}")

    r = range(a, b+1)

    ptwo = sum(check(x, mode=2) for x in r)

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
