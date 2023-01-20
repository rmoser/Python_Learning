# Advent of Code
year = 2017
day = 15

import numpy as np
import aocd

text0 = """
Generator A starts with 65
Generator B starts with 8921
"""
text1 = aocd.get_data(day=day, year=year)


def gen(x, x_mul, f):
    while True:
        x = (x * x_mul) % 2147483647
        if (x % f) == 0:
            return x


def count(a, b, n=40000000, pone=True):
    a_mul = 16807
    b_mul = 48271
    d = 2147483647
    total = 0
    for _ in range(n):
        if pone:
            a = gen(a, a_mul, 1)
            b = gen(b, b_mul, 1)
        else:
            a = gen(a, a_mul, 4)
            b = gen(b, b_mul, 8)

        if (a & 65535) == (b & 65535):
            # print(a & 65535, b & 65535)
            total += 1
    return total


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip()
    if '\n' in text:
        text = text.splitlines()

    a, b = [int(line.split()[-1]) for line in text]

    # print(a, b)

    pone = count(a, b)

    print(f"AOC {year} day {day}  Part One: {pone}")

    ptwo = count(a, b, n=5000000, pone=False)
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
