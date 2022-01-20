# Advent of Code
year = 2017
day = 7

import numpy as np
import aocd
from scipy.stats import mode

text0 = """
pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)
"""
text1 = aocd.get_data(day=day, year=year)


def weigh(node, network, weights, net_weights):
    if node in net_weights:
        return net_weights[node]

    net_weight = weights[node] + sum(weigh(n, network, weights, net_weights) for n in network[node])
    if node not in net_weights:
        net_weights[node] = net_weight
    return net_weight


def is_imbalanced(node, network, weights, net_weights):
    # Returns False if the node is balanced
    # Else returns the name of the imbalanced node
    if not network[node]:
        return False, 0
    sub_nodes = network[node]
    w = np.zeros((2, len(sub_nodes)), dtype=object)
    w[0] = list(sub_nodes)
    w[1] = [weigh(n, network, weights, net_weights) for n in w[0]]
    m = mode(w[1]).mode[0]

    odd_ball = w[1] != m
    if odd_ball.any():
        i = odd_ball.argmax()
        return w[0, i], m - w[1, i]  # Returns the name of the bad node, and what additional weight would balance it
    return False, 0


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    weights = dict()
    network = dict()
    net_weights = dict()

    for line in text:
        if " -> " in line:
            info, rest = line.split(" -> ")
            rest = set(rest.split(', '))
        else:
            info = line
            rest = set()
        disc, weight = info.split()
        weight = int(weight[1:-1])
        weights[disc] = weight
        network[disc] = rest

    # print(weights)
    # print(network)

    for disc in network:
        if not any(disc in v for v in network.values()):
            pone = disc
            break

    print(f"AOC {year} day {day}  Part One: {pone}")

    weigh(pone, network, weights, net_weights)

    node = pone
    while True:
        check, offset = is_imbalanced(node, network, weights, net_weights)

        # Walk the tree until we hit the lowest imbalanced node
        # print(node, check, offset, is_imbalanced(check, network, weights, net_weights))
        if check and network[check] and is_imbalanced(check, network, weights, net_weights)[0]:
            node = check
            continue

        # Find the delta between the imbalanced node
        ptwo = offset + weights[check]
        break



    print(f"AOC {year} day {day}  Part Two: {ptwo}")
