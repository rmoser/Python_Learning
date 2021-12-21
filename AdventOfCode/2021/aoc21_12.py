# Advent of Code
year = 2021
day = 12

import numpy as np
import aocd

text0 = """
start-A
start-b
A-c
A-b
b-d
A-end
b-end
"""

text01 = """
dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc
"""

text1 = aocd.get_data(day=day, year=year)


def read_net(s):
    d = dict()
    for line in s:
        a, b = line.split("-")
        # print(a, b)
        if a not in d:
            d[a] = set()
        if a != 'end' and b != 'start':
            d[a].add(b)

        if b not in d:
            d[b] = set()
        if b != 'end' and a != 'start':
            d[b].add(a)

    return d


def map_chain3(d, base=None, done=None, small_cave_repeat_limit=0, iters=-1):
    node_enum = ['start', 'end']
    node_dict = {'start': 0, 'end': 1}
    small_caves = [False, False]
    large_caves = [False, False]

    middle_nodes = [x for x in np.unique(list(d.keys())) if x not in node_enum]
    for i, node in enumerate(sorted(middle_nodes)):
        node_enum.append(node)
        node_dict[node] = i + 2
        small_caves.append(node.islower())
        large_caves.append(node.isupper())

    if not isinstance(list(d.keys())[0], str):
        _d = d
    else:
        _d = dict()
        for k, v in d.items():
            # print(k, v)
            _d[node_dict[k]] = {node_dict[x] for x in v}

    # print(_d)

    # print(node_enum, node_dict)

    if base is None:
        base = [[0]]
    if done is None:
        done = []
    # print(f"base: {base}")

    # print(base)

    while iters != 0:
        for i in range(len(base)-1, -1, -1):
            chain = base.pop(i)
            node = chain[-1]
            for next_node in _d[node]:
                new_chain = chain.copy()
                new_chain.append(next_node)
                # print(new_chain)
                if next_node == 1:
                    done.append(new_chain)
                    continue
                if next_node > 1 and valid_chain(new_chain, small_caves, small_cave_repeat_limit):
                    base.append(new_chain)

        iters -= 1
        # print(f"{iters}: base {len(base)}, done {len(done)}")

        if len(base) == 0:
            break

    return _d, base, done


def valid_chain(chain, small_caves, small_cave_repeat_limit=0):
    # print(f"chain: {chain}")
    # print(f"small_caves: {small_caves}")
    nodes = np.unique(chain)
    small_node_counts = [chain.count(node) for node in nodes if small_caves[node]]
    counts = [x for x in small_node_counts if x > 1]

    if any([c > 2 for c in counts]):
        return False
    return len(counts) <= small_cave_repeat_limit


def print_chain(chain, enum):
    print([enum[c] for c in chain])


if __name__ == '__main__':
    pone = 0
    ptwo = 0

    text = text1
    text = text.strip().splitlines()
    d = read_net(text)
    # print(d)

    net1 = map_chain3(d, iters=-1)
    pone = len(net1[2])

    net2 = map_chain3(d, iters=-1, small_cave_repeat_limit=1)
    ptwo = len(net2[2])

    print(f"AOC {year} day {day}  Part One: {pone}")
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
