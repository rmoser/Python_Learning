# Advent of Code
year = 2024
day = 23

import numpy as np
import aocd
import os
import itertools as it
# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

text0 = """
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
"""
text1 = aocd.get_data(day=day, year=year)

def combinations(computers, n=2):
    result = []
    for group in it.combinations(sorted(computers.keys()), n):
        _group = set(group)
        if all(len(computers[g] & _group) == n-1 for g in _group):
            result.append(group)
    return result

def connected(node, nodes, computers):
    return bool(set(nodes) & computers[node] == set(nodes))

def interconnected(nodes, computers):
    return all((set(nodes)).issubset(computers[c]) for c in nodes)

def extend(start, computers):
    result = []
    if not start:
        start = list({x} for x in computers.keys())

    for network in start:
        for n in network:
            for c in computers[n] - network:
                new = network | {c}
                if new not in result and connected(c, network, computers):
                    result.append(new)
    return result

def map_networks(computers):
    start = [c for c in computers if c.startswith('t')]
    result = list(list() for _ in computers)
    for c in start:
        d = dict()
        net = computers[c]
        for node in net - {c}:
            x = net & computers[node]
            if interconnected(x, computers):
                d[node] = len(x)
            else:
                for n in range(len(x)-1, 0, -1):
                    for group in it.combinations(x, n):
                        if interconnected(group, computers):
                            d[node] = n
                            break
                    else:
                        continue
                    break
                else:
                    continue
                break

        n_max = max(d.values())
        keep = [c] + [x for x in d if d[x] == n_max]
        new = tuple(sorted(keep))
        if new not in result[n_max]:
            result[n_max].append(new)

    return result

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    computers = dict()
    for line in text:
        a, b = line.split('-')
        if a not in computers:
            computers[a] = set()
        if b not in computers:
            computers[b] = set()
        computers[a].add(a)
        computers[a].add(b)
        computers[b].add(a)
        computers[b].add(b)

    triplets = extend(None, computers)  # Two
    triplets = extend(triplets, computers)  # Three

    pone = sum(any(x.startswith('t') for x in t) for t in triplets )

    print(f"AOC {year} day {day}  Part One: {pone}")

    network = map_networks(computers)
    while not network[-1]:
        network.pop(-1)

    ptwo = ','.join(sorted(network[-1][0]))

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
