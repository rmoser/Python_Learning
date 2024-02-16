# Advent of Code
year = 2022
day = 16

import numpy as np
import aocd
import itertools
import collections
import functools

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


class memoized(object):
    '''Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated).
    '''

    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        if not isinstance(args, collections.Hashable):
            # uncacheable. a list, for instance.
            # better to not cache than blow up.
            return self.func(*args)
        if args in self.cache:
            return self.cache[args]
        else:
            value = self.func(*args)
            self.cache[args] = value
            return value

    def __repr__(self):
        '''Return the function's docstring.'''
        return self.func.__doc__

    def __get__(self, obj, objtype):
        '''Support instance methods.'''
        return functools.partial(self.__call__, obj)


class Valve(object):
    Valves = dict()

    def __init__(self, name, rate, conn):
        self.name = name
        self.rate = rate
        self.conn = tuple(conn)
        self.distances = dict()
        self.Valves[name] = self


def calculate_distances(valves, length=None):
    distances = dict()
    n_valves = len(valves)
    end_condition = n_valves * (n_valves-1)

    if length is None or length <= 0:
        length = n_valves

    # Add paths with length 1
    for name, valve in valves.items():
        for _v in valve.conn:
            distances[(name, _v)] = 1

    # Add longer new paths until we reach distance l
    for _ in range(2, length):
        for (a, b), d in tuple(distances.items()):
            for c in valves[b].conn:
                if a == c:
                    continue
                # print(a, b, c)
                if (a, c) not in distances:
                    distances[(a, c)] = d + 1
                    distances[(c, a)] = d + 1

        if len(distances) == end_condition:
            break

    # for start, end in itertools.combinations(valves, 2):
    #     remainder = set(valves) - set((start, end))
    #     for l in length:
    #         for path in itertools.permutations(remainder, l-1):
    #             if all(b in valves[a].conn for a, b in zip(path[:-1], path[1:])):
    #                 distances[(start, end)] = l
    #                 distances[(end, start)] = l
    #                 break
    #         if (start, end) in distances:
    #             break

        #     if len(distances) == end_condition:
        #         break
        #
        # if len(distances) == end_condition:
        #     break

    for (start, end), value in distances.items():
        valves[start].distances[end] = value

    return distances


def valid_paths(start, valves):
    required_valves = [v for v in valves if valves[v].rate > 0 and v != start]

    for x in itertools.permutations(required_valves, len(required_valves)):
        yield (start,) + x


def score(path, valves, time=0, debug=False):
    if not hasattr(score, 'memo'):
        score.memo = {}

    if (path, time) in score.memo:
        print(f"\n\n\nMemo: {path} {time} {score.memo[path, time]}\n\n\n")
        return score.memo[path, time]

    if any(not valves[v].distances for v in valves):
        calculate_distances(path[0], valves)

    total = 0

    a, path = path[0], path[1:]
    elapsed_time = min(valves[a].distances[path[0]] + 1, time)
    if elapsed_time >= time:  # No more moves will score
        for i in range(time+1):
            score.memo[path, i] = total
        return total

    if time < 0:
        raise ValueError(f"Invalid time remaining: {time}")

    total = valves[a].rate * (time-elapsed_time) + score(path, valves, time - elapsed_time)
    score.memo[path, time] = total
    return total


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
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

    calculate_distances(valves)
    time = 30
    pos = 'AA'

    best_move = (0, None)
    i = 0
    for moves in valid_paths(pos, valves):
        i += 1
        if i < 1000 or i < 1000000 and i % 1000 == 0 or i % 100000 == 0:
            print(f"\r{i}", len(score.__dict__.get('memo', '')), '              ', end='')
        # print(moves)
        s = score(moves, valves, time)
        if s > best_move[0]:
            best_move = (s, moves)
            print(f"\r{i} {best_move}")
        # print(moves, s)

    print(best_move)
    score(best_move[1], valves, debug=True)
    pone = best_move[0]
    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
