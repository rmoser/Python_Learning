# Advent of Code
year = 2018
day = 5

import numpy as np
import aocd

text0 = """dabAcCaCBAcCcaDA"""
text1 = aocd.get_data(day=day, year=year)


def check(a, b):
    return abs(ord(a) - ord(b)) == 32


def reduce(s):
    s = list(s)
    result = ''
    a = 0
    b = 1
    while b < len(s):
        # print(a, b, s[max(0, a-2):min(len(s), b+2)])
        if s[a] == '_':
            a = b
            b += 1
            continue

        if check(s[a], s[b]):
            s[a] = '_'
            s[b] = '_'
            while s[a] == '_':
                a -= 1
            b += 1
            if a == -1:
                a = b
                b += 1
            result = result[:-1]
        else:
            result += s[a]
            a = b
            b += 1
        # print(a, b, s[max(0, a-2):min(len(s), b+2)])
        # input()

    if s[a] != '_':
        result += s[a]
    return result


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip()
    if '\n' in text:
        text = text.splitlines()

    pone = len(reduce(text))

    d = dict()
    for i in range(26):
        C = chr(65+i)
        c = chr(97+i)

        r = text1.replace(c, '').replace(C, '')
        d[len(reduce(r))] = c

    ptwo = min(d)

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
