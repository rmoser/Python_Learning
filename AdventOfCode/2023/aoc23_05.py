# Advent of Code
year = 2023
day = 5

import numpy as np
import aocd
import os
os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"

text0 = """
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""
text1 = aocd.get_data(day=day, year=year)


# def gen_map(text):
#     map = dict()
#     for line in text:
#         dest, src, rng = (int(x) for x in line.split())
#         for i in range(rng):
#             map[src+i] = dest+i
#     for i in range(max(map.keys())):
#         if i not in map:
#             map[i] = i
#     return map
#
#
# def update_map(a, b):
#     m = dict()
#     for k, v in a.items():
#         m[k] = b[v]
#     return m


def proc_map(value, map):
    for line in map:
        # dest, src, rng = line
        min, max, offset = line
        if min <= value < max:
            return value + offset
    return value


def combine_maps(a, b):
    m = list()
    for aline in a:
        a_min, a_max, a_offset = aline

        for bline in b:
            b_min, b_max, b_offset = bline

            m_offset = a_offset + b_offset
            m_min = a_min

            if b_min <= a_min + a_offset < b_max:
                m_min = a_min
                m_max = min(a_max, b_max-a_offset)
                m_offset = a_offset + b_offset
                m.append(m_min, m_max, m_offset)
                if m_max < a_max:
                    m_min = m_max
                    m_max =

def translate_map(map):
    m = []
    for line in map:
        dest, src, rng = line
        m.append((src, src+rng, dest-src))
    m.sort()
    return m


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    maps = dict()
    text = text1
    text = text.strip().splitlines()

    d = ""
    seeds = []
    for line in text:
        if line.startswith("seeds"):
            seeds = [int(x) for x in line.split(":")[1].split()]
            continue

        if line.endswith("map:"):
            d = line.split()[0]
            # print(d)
            continue

        if not line:
            d = ""
            continue

        record = tuple(int(x) for x in line.split())

        if d:
            # print(record)
            if d not in maps:
                maps[d] = list()
            maps[d].append(record)

    map_names = ["seed-to-soil"]
    while len(map_names) < len(maps):
        m = map_names[-1].split('-')[-1]
        for name in maps:
            if name.startswith(m):
                map_names.append(name)

    for name, map in maps.items():
        maps[name] = translate_map(map)

    print(seeds)
    locations = []
    for seed in seeds:
        for map in map_names:
            seed = proc_map(seed, maps[map])
            # print(map, seed)
        locations.append(seed)

    pone = np.array(locations).min()

    print(f"AOC {year} day {day}  Part One: {pone}")

    seeds = list(zip(seeds[::2], seeds[1::2]))
    print(seeds)



    print(f"AOC {year} day {day}  Part Two: {ptwo}")
