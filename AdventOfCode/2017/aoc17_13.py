# Advent of Code
year = 2017
day = 13

import numpy as np
import aocd

text0 = """
0: 3
1: 2
4: 4
6: 4
"""
text1 = aocd.get_data(day=day, year=year)


def pos(i, n):
    d = 2 * n - 2
    r = i % d
    if r+1 > n:
        r = d - r
    return r


def score(start, firewall):
    caught = False
    result = 0
    for i in firewall:
        t = i + start
        if pos(t, firewall[i]) == 0:
            caught = True
            # print(t, i, firewall[i])
            result += i * firewall[i]
    return caught, result


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    firewall = dict()
    for line in text:
        i, d = (int(c) for c in line.split(': '))
        firewall[i] = d

    _, pone = score(0, firewall)

    print(f"AOC {year} day {day}  Part One: {pone}")

    i = 1
    while True:
        if i % 10000 == 0:
            print(i)
        caught, x = score(i, firewall)
        if not caught:
            ptwo = i
            break
        i += 1

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
