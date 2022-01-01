# Advent of Code
year = 2015
day = 20

import numpy as np
import aocd
import itertools

text0 = """ 
"""
text1 = aocd.get_data(day=day, year=year)

# From wimglenn...this seems like brute force, but so much faster than what I did
if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    target = int(text[0])

    A = np.zeros(1000000, dtype=int)
    B = A.copy()
    for i in range(1, 1000000):
        A[i::i] += i * 10
        B[i::i][:50] += i * 11

    pone = np.argmax(A > target)
    ptwo = np.argmax(B > target)

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
