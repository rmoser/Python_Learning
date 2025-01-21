# Advent of Code
year = 2017
day = 24

import numpy as np
import aocd
import os
from pprint import pprint
import itertools as it
import utils
import functools

# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

text0 = """
0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10
"""
text1 = aocd.get_data(day=day, year=year)

@functools.cache
def valid(bridge: tuple) -> bool:
    if len(bridge) <= 1:
        return 0 in bridge
    if len(bridge) == 2:
        a, b = bridge
        return 0 in a and max(a) in b

    result = True
    if not valid(bridge[:2]):
        return False

    for a, b, c in zip(bridge[2:], bridge[1:-1], bridge[:-2]):
        x, y = b
        if not (x in a and y in c or x in c and y in a):
            result = False
    return result

def score(bridge: tuple) -> int:
    if not valid(bridge):
        return 0
    return sum(a for x in bridge for a in x)

def build_bridges(valid_components):
    stack = [((0, 0), )]

    while stack:
        # print(len(stack))
        bridge = stack.pop()
        yield bridge

        for c in (valid_components[bridge[-1][0]] | valid_components[bridge[-1][1]]) - set(bridge):
            new = bridge + (c, )
            if valid(new):
                stack.append(new)



if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    components = []
    for line in text:
        a, b = line.split('/')
        components.append((int(a), int(b)))

    valid_components = dict()
    for component in components:
        # print(component)
        a, b = component
        if a not in valid_components:
            valid_components[a] = set()
        valid_components[a].add(component)
        if b not in valid_components:
            valid_components[b] = set()
        valid_components[b].add(component)

    pone = 0
    ptwo = 0
    ptwo_bridge = ((0, 0), )
    for b in build_bridges(valid_components):
        s = score(b)
        if s > pone:
            pone = s
        if len(b) > len(ptwo_bridge):
            ptwo_bridge = b
            ptwo = s
        elif len(b) == len(ptwo_bridge) and s > ptwo:
            ptwo_bridge = b
            ptwo = s

    print(f"AOC {year} day {day}  Part One: {pone}")
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
