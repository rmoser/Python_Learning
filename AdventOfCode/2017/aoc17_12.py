# Advent of Code
year = 2017
day = 12

import numpy as np
import aocd

text0 = """
0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5
"""
text1 = aocd.get_data(day=day, year=year)

net = dict()


def in_group(n):
    s = set([n])
    nodes = set(net[n]) - s
    while nodes:
        node = nodes.pop()
        s |= set([node])
        nodes |= (set(net[node]) - s)

    return s


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    for line in text:
        node, connections = line.split(' <-> ')
        node = int(node)
        connections = [int(c) for c in connections.split(', ')]
        net[node] = connections

    # print(net)

    s = in_group(0)
    # print(s)
    pone = len(s)

    groups = []

    for n in net:
        if any(n in x for x in groups):
            continue
        s = in_group(n)
        groups.append(s)

    ptwo = len(groups)


    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
