# Advent of Code
year = 2015
day = 9

import numpy as np
import itertools
import aocd

text0 = """
London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141
"""
text1 = aocd.get_data(day=day, year=year)


def calc_route(route, distances):
    return sum(distances[f"{a}.{b}"] for a, b in zip(route[:-1], route[1:]))


if __name__ == '__main__':
    text = text1.strip().splitlines()
    d = dict()
    cities = dict()
    for t in text:
        c0, _, c1, _, dist = t.split()
        dist = int(dist)
        d[f"{c0}.{c1}"] = dist
        d[f"{c1}.{c0}"] = dist
        cities[c0] = 1
        cities[c1] = 1

    print(cities)
    print(d)

    routes = list(itertools.permutations(cities.keys()))
    distances = [calc_route(r, d) for r in routes]

    print(f"AOC {year} day {day}  Part One: {min(distances)}")

    print(f"AOC {year} day {day}  Part Two: {max(distances)}")
