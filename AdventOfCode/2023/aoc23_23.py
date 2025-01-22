# Advent of Code
year = 2023
day = 23

import numpy as np
import aocd
import os
# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
import igraph as ig
import matplotlib.pyplot as plt
import utils
from pprint import pprint
import logging, sys
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
import itertools as it
import functools


text0 = """
#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
"""
text1 = aocd.get_data(day=day, year=year)

DIRS = {'E': (0, 1), 'W': (0, -1), 'N': (-1, 0), 'S': (1, 0)}
EXITS = {'E': '>', 'W': '<', 'N': '^', 'S': 'v'}
ENTRIES = {'E': '<', 'W': '>', 'N': 'v', 'S': '^'}

@functools.cache
def longest_path(a, b):
    dist = 0


def exits(pos, arr):
    global DIRS
    p = np.array(pos)
    result = []
    for d in DIRS.keys():
        # if (p == [22, 21]).all():
        #     logging.debug(p, d, DIRS[d])
        _p = p + DIRS[d]
        if np.all(np.bitwise_and((0, 0) <= _p, _p < arr.shape)) and arr[tuple(p + DIRS[d])] in ('.', '>', 'v', '^'):
            result.append((d, tuple(int(i) for i in _p)))
    return result

def walk(pos, arr):
    global EXITS
    is_exit = None
    _p = pos[-1]
    if isinstance(_p, Node):
        _p = _p.pos
    path = [p.pos if isinstance(p, Node) else p for p in pos]

    while True:
        e = exits(_p, arr)
        if len(e) != 2:
            return path[1:], is_exit
        for _n in e:
            if arr[tuple(_n[1])] == EXITS[_n[0]] or arr[_p] == EXITS[_n[0]]:
                is_exit = True
            elif arr[tuple(_n[1])] == ENTRIES[_n[0]] or arr[_p] == ENTRIES[_n[0]]:
                is_exit = False
            if tuple(_n[1]) not in path:
                _p = tuple(_n[1])
                break
        path.append(_p)


def get_index(pos, arr):
    return arr.shape[0] * pos[0] + pos[1]

def get_pos(index, arr):
    return divmod(index, arr.shape[0])


class Node(object):
    def __init__(self, pos: tuple, entry: dict = None):
        self.pos = tuple(int(i) for i in pos)
        self.entry = entry if entry else set()
        self.exit = dict()

    def __hash__(self):
        return hash(self.pos)

    def __eq__(self, other):
        return (self.pos,) == (other.pos,)

    def __str__(self):
        return str(self.pos)

    def __repr__(self):
        return str(f'Node {self.pos}:  Entries: {[e.pos for e in self.entry]} Exits: {[e.pos for e in self.exit]}')

    def add_entry(self, new):
        self.entry.add(new)

    def add_exit(self, new, distance: int = None):
        self.exit[new] = distance

    def to_next(self):
        for x in self.exit.items():
            yield x

    def to_node(self, pos):
        if isinstance(pos, Node):
            pos = pos.pos
        for n, dist in self.to_next():
            if n.pos == pos:
                return dist
            return dist + n.to_node(pos)



if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    arr = np.array([[c for c in line] for line in text])
    nodes = dict()
    # g = ig.Graph()
    # g.add_vertices(np.prod(arr.shape))

    start = Node((0, 1))
    end = None
    nodes[start.pos] = start


    for n in zip(*np.where(arr != '#')):
        if n in nodes:
            continue
        n = tuple(int(i) for i in n)
        e = exits(n, arr)
        if len(e) > 2:
            nodes[n] = Node(n)
            continue
        if n[0] == arr.shape[0]-1:
            end = Node(n)
            nodes[n] = end

    logging.debug(f'\nStart {start} -> End {end}')

    path = set(start.pos)

    logging.debug('debug')
    for i, node in enumerate(nodes.values()):
        logging.debug(f"{i} / {len(nodes)}: {node}")
        path.add(node.pos)
        for exit in exits(node.pos, arr):
            e = tuple(exit[1])
            if e not in path:
                p, is_exit = walk((node, e), arr)
                logging.debug(f"walk(({node.pos}, {e}), arr) : {p[-1]} {is_exit}")
                for n in p:
                    path.add(n)
                # j = g.add_edge(get_index(node, arr), get_index(n, arr))
                # g.es[j.index]['weight'] = len(p)
                N = nodes[p[-1]]
                if is_exit != True:
                    N.add_exit(node, len(p))
                    node.add_entry(N)
                elif is_exit != False:
                    node.add_exit(N, len(p))
                    N.add_entry(node)
        logging.debug(node.__repr__() + '\n')

    # pprint(nodes)
    paths_work = [[start]]
    paths = []

    while paths_work:
        p = paths_work.pop()
        for n in p[-1].exit:
            if n == end:
                paths.append(p + [n])
            else:
                paths_work.append(p + [n])
        logging.debug(len(paths_work))

    path_distances = []
    for p in paths:
        # for a, b in zip(p[:-1], p[1:]):
        #     print(a, b, a.exit[b])
        path_distances.append(sum((a.exit[b] for a, b in zip(p[:-1], p[1:]))))

    # print(path_distances)
    pone = max(path_distances)

    print(f"AOC {year} day {day}  Part One: {pone}")


    # pprint(nodes)
    paths_work = {(start.pos, )}
    paths = set()

    while paths_work:
        p = paths_work.pop()
        for n in list(nodes[p[-1]].exit) + list(nodes[p[-1]].entry):
            if n.pos in p:
                continue
            _p = p + (n.pos, )
            if n == end:
                paths.add(_p)
            else:
               paths_work.add(_p)
        logging.debug(len(paths_work))

        if len(paths_work) > 1000:
            break

    path_distances = []
    for p in paths:
        # for a, b in zip(p[:-1], p[1:]):
        #     print(a, b, a.exit[b])
        path_distances.append(sum((a.exit[b] if b in a.exit else b.exit[a] for a, b in zip(p[:-1], p[1:]))))

    ptwo = max(path_distances)

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
