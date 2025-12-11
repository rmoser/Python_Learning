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

text0 = """svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out"""

text1 = aocd.get_data(day=day, year=year)

Network = dict()

@functools.cache
def paths_to(node, end='out'):
    if node not in Network:
        return 0
    if end in Network[node]:
        return 1
    return sum(paths_to(n, end) for n in Network[node])


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

    pone = paths_to('you')
    print(f"AOC {year} day {day}  Part One: {pone}")

    fft_dac = paths_to('fft', 'dac')
    if fft_dac == 0:
        ptwo = paths_to('svr', 'dac') * paths_to('dac', 'fft') * paths_to('fft', 'out')
    else:
        ptwo = paths_to('svr', 'fft') * fft_dac * paths_to('dac', 'out')

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
