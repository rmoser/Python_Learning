# Advent of Code
year = 2022
day = 16

import numpy as np
import aocd
import itertools

text0 = """
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
"""
text1 = aocd.get_data(day=day, year=year)


class Valve(object):
    Valves = dict()

    def __init__(self, name, rate, conn):
        self.name = name
        self.rate = rate
        self.conn = tuple(conn)
        self.distances = dict()
        self.Valves[name] = self


def calculate_distances(valves, length=np.inf):
    distances = dict()
    n_valves = len(valves)

    l = 1
    while len(distances) < n_valves * (n_valves-1) and l <= length:
        l += 1
        for path in itertools.combinations(valves.keys(), l):
            start = path[0]
            end = path[-1]
            if (start, end) in distances:  # Found a shorter path already
                continue
            if all(b in valves[a].conn for a, b in zip(path[:-1], path[1:])):
                distances[(start, end)] = len(path) - 1

    for (start, end), value in distances.items():
        valves[start].distances[end] = value
        valves[end].distances[start] = value

    return distances


def valid_paths(start, valves):
    required_valves = [v for v in valves if valves[v].rate > 0 and v != start]

    yield ((start,) + x for x in itertools.permutations(required_valves, len(required_valves)))

    # for _ in range(length):
    #     for i in range(len(paths)):
    #         path = paths.pop(0)
    #         pos = valves[path[-1]]
    #
    #         # All useful valves are already on, so just wait
    #         if all(f"'{x}', '{x}'" in str(path) for x in required_valves):
    #             paths.append(path + [pos.name])
    #             continue
    #
    #         for new_pos in pos.conn:
    #             if len(path) <= 1 or new_pos != path[-2]:
    #                 paths.append(path + [new_pos])
    #
    #         if pos.rate > 0 and f"'{pos.name}', '{pos.name}'" not in str(path):
    #             paths.append(path + [pos.name])
    # return paths


def score(path, valves, time=0, debug=False):
    if any(not valves[v].distances for v in valves):
        calculate_distances(path[0], valves)

    total = 0
    score_per_second = 0
    for a, b in zip(path[:-1], path[1:]):
        elapsed_time = min(valves[a].distances[b] + 1, time)

        total += score_per_second * elapsed_time
        time -= elapsed_time
        score_per_second += valves[b].rate

        if time < 0:
            raise ValueError(f"Invalid time remaining: {time}")

        if time == 0:
            break

    return total

    # pos = path[0]
    # total = 0
    # valve_states = {x: False for x in valves.keys()}
    # for _pos in path[1:]:
    #     _score = sum(v.rate for v in valves.values() if valve_states[v.name])
    #     total += _score
    #
    #     if debug:
    #         print(pos, _pos, [x for x in valves if valve_states[x]], total, _score)
    #     if _pos == pos:
    #         valve_states[pos] = True
    #     elif _pos not in valves[pos].conn:
    #         return 0
    #
    #     pos = _pos
    #
    # return total


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text0
    text = text.strip().splitlines()

    valves = None
    for line in text:
        a, b = line.split('; ')
        a = a.split(' ')
        n = a[1]
        r = int(a[4].split('=')[1])
        b = [x.strip() for x in b.split('to ')[1][6:].split(', ')]
        v = Valve(n, r, b)
        valves = v.Valves

    time = 30
    pos = 'AA'

    best_move = (0, None)
    for moves in valid_paths(pos, valves, time):
        s = score(moves, valves)
        if s > best_move[0]:
            best_move = (s, moves)
        print(moves, s)

    print(best_move)
    score(best_move[1], valves, debug=True)
    pone = best_move[0]
    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
