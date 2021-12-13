# Advent of Code
year = 2015
day = 11

import numpy as np
import aocd

text0 = "abcdefgh"
text1 = aocd.get_data(day=day, year=year)


def is_valid(p):
    # Invalid chars
    if any(c in p for c in ('i','o','l')):
        return False

    # Straights
    _p = [ord(c) for c in p]
    triplets = zip(_p[:-2], _p[1:-1], _p[2:])
    if not any((a+2 == b+1 == c) for a, b, c in triplets):
        return False

    # Runs
    doublets = zip(p[:-1], p[1:])
    d = dict()
    for a, b in doublets:
        if a == b:
            d[a] = 1
    return len(d.keys()) > 1


def increment(p):
    _p = [ord(c) for c in p]
    _p[-1] += 1
    while _p[-1] in (105, 106, 111):
        _p[-1] += 1

    for i in range(-1, -len(p), -1):
        if _p[i] > 122:
            _p[i] = 97
            _p[i-1] += 1
            while _p[i-1] in (105, 106, 111):
                _p[i-1] += 1
    return "".join(chr(c) for c in _p)


if __name__ == '__main__':
    text = text1

    p = increment(text)
    while not is_valid(p):
        p = increment(p)

    print(f"AOC {year} day {day}  Part One: {text} -> {p}")

    p = increment(p)
    while not is_valid(p):
        p = increment(p)

    print(f"AOC {year} day {day}  Part Two: {p}")
