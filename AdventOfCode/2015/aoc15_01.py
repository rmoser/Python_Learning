# Advent of Code
year = 2015
day = 1

import numpy as np
import aocd

text0 = "((()"
text1 = aocd.get_data(day=day, year=year)

text = text1
incs = np.array([1 if c == '(' else -1 for c in text])

print(f"AOC {year} day {day}  Part One: {incs.sum()}")

sums = incs.cumsum()
print(f"AOC {year} day {day}  Part Two: {1 + np.where(sums==-1)[0][0]}")
