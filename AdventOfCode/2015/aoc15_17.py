# Advent of Code
year = 2015
day = 17

import numpy as np
import aocd
import itertools

text0 = """
20
15
10
5
5
"""
text1 = aocd.get_data(day=day, year=year)


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    conts = np.array([int(x) for x in text])

    combs = itertools.product((0, 1), repeat=len(conts))

    container_count = 150
    count_one = 0
    count_two = 0
    for comb in combs:
        comb = np.array(comb)
        if (comb * conts).sum() == 150:
            count_one += 1
            if comb.sum() < container_count:
                container_count = comb.sum()
                count_two = 1
            elif comb.sum() == container_count:
                count_two += 1

    pone = count_one
    print(f"AOC {year} day {day}  Part One: {pone}")


    ptwo = count_two
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
