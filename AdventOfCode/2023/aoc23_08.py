# Advent of Code
year = 2023
day = 8

import numpy as np
import aocd
import utils
import math

text0 = """
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""

text0 = """
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""

text1 = aocd.get_data(day=day, year=year)


def move(node, nodes=None, counter=0):
    while True:
        for i in inst:
            counter += 1
            node = nodes[node][i]
            if node == 'ZZZ':
                return counter


def move_az(node_list, nodes=None, counter=0):
    while True:
        for i in inst:
            counter += 1
            for n, node in enumerate(node_list):
                node = nodes[node][i]
                node_list[n] = node
            if all((node.endswith('Z') for node in node_list)):
                return counter, node_list


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    inst = text[0]
    inst = [int(c == 'R') for c in inst]

    nodes = {}
    for line in text[2:]:
        line = ''.join([c for c in line if c.isalpha() or c == ' ']).split()
        nodes[line[0]] = line[1:]

    print(inst)
    print(nodes)

    node = 'AAA'  # Start node
    pone = move(node, nodes)

    print(f"AOC {year} day {day}  Part One: {pone}")

    node_list = [n for n in nodes.keys() if n.endswith('A')]

    data = []
    for node in node_list:
        data.append(move_az([node], nodes))

    factors = [utils.factor(x[0]) for x in data]
    data = {}
    for d in factors:
        for k, v in d.items():
            if v > data.get(k, 0):
                data[k] = v
    ptwo = math.prod([k ** v for k, v in data.items()])

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
