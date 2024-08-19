# Advent of Code
year = 2023
day = 5

import numpy as np
import aocd
import os
import pprint
import collections as coll

os.environ[
    "AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"

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


# Combine different rules for a single map
# New map offset values override existing values
def parse_map(a):
    m = [[], []]
    for start, count, offset in a:
        start_flag = -1
        end_flag = -1
        for i, v in enumerate(m[0]):
            if get_map_offset(start, m) != 0:
                if v > start:
                    start_flag = i

            if get_map_offset(start+count, m) == 0:
                if v < start + count:
                    end_flag = i

            if start_flag >= 0:
                m[0].insert(start_flag, start)
                m[1].insert(start_flag, offset)
            else:
                m[0].append(start)
                m[1].append(offset)

    return m


def get_map_offset(id, m):
    for i in range(len(m[0])-1):
        # print(f"{m[0][i]} <= {id} < {m[0][i+1]}")
        if m[0][i] <= id < m[0][i+1]:
            return m[1][i]
    return 0


def get_map_value(id, m):
    return id + get_map_offset(id, m)


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    maps = dict()
    text = text0
    text = text.strip().splitlines()

    label = ''
    nums = []
    d = coll.OrderedDict()

    order = ("seed-to-soil", "soil-to-fertilizer", "fertilizer-to-water", "water-to-light", "light-to-temperature",
             "temperature-to-humidity", "humidity-to-location")

    order = order[:1]

    for line in text:
        if line.startswith("seeds:"):
            d['seeds'] = np.array(line.split()[1:], dtype=np.int64)
            continue

        if line.endswith("map:"):
            label = line.split()[0]
            print(label)
            continue

        if line and label:
            l = d.get(label, [])
            min, max, value = np.array(line.split(), dtype=np.int64)
            max = min + max
            l.insert(0, [min, max, value])
            d[label] = l
            continue

        if not line:
            label = ''
            continue

    # l = {}
    # for a, b in zip(d['seeds'][::2], d['seeds'][1::2]):
    #     l[a] = 0
    #     l[]
    #     l.append(tuple(np.array([a[0], a[0] + b[0], 0], dtype=np.int64)))
    #     d['seeds_1'] = l

    pprint.pprint(d)

    map = [d['seeds'].copy(), [0] * len(d['seeds'])]
    pprint.pprint(map)

    for o in order:
        print(o)
        for i in range(len(map)):
            a = map.pop(0)
            for b in d[o]:
                for m in merge_map(a, b):
                    if m not in map:
                        map.append(m)


        pprint.pprint(map)

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
