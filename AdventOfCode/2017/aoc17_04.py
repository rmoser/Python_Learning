# Advent of Code
year = 2017
day = 4

import numpy as np
import aocd

text0 = """
aa bb cc dd ee
aa bb cc dd aa
aa bb cc dd aaa
"""
text1 = aocd.get_data(day=day, year=year)


def is_valid(password, dosort=False):
    d = dict()
    for word in password.split():
        if dosort:
            word = ''.join(sorted(word))
        if word in d:
            return False
        d[word] = 0

    return True


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    pone = sum(is_valid(x) for x in text)

    print(f"AOC {year} day {day}  Part One: {pone}")

    ptwo = sum(is_valid(x, True) for x in text)

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
