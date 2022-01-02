# Advent of Code
year = 2016
day = 6

import numpy as np
import aocd

text0 = """
eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar
"""
text1 = aocd.get_data(day=day, year=year)


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    arr = np.array([list(x) for x in text])

    for r in range(arr.shape[1]):
        chars, counts = np.unique(arr[:, r], return_counts=True)
        pone += chars[counts.argmax()]
        ptwo += chars[counts.argmin()]


    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
