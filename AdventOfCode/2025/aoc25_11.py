from __future__ import annotations

# Advent of Code
year = 2025
day = 11

import functools
import numpy as np
import aocd
import os
import utils
from pprint import pprint
from icecream import ic

text0 = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
"""
text1 = aocd.get_data(day=day, year=year)

Network = dict()

@functools.cache
def paths_to_out(node):
    if node not in Network:
        return 0
    if 'out' in Network[node]:
        return 1
    return sum(paths_to_out(n) for n in Network[node])

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    network = Network
    for line in text:
        _in, _out = line.split(': ')
        _out = set(_out.strip().split())
        network[_in] = _out
    ic(network)

    pone = paths_to_out('you')
    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
