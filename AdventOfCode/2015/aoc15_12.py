# Advent of Code
year = 2015
day = 12

import numpy as np
import aocd
import json


text0 = """
[
[1,2,3],
{"a":2,"b":4},
[[[3]]],
{"a":{"b":4},"c":-1},
{"a":[-1,1]},
[-1,{"a":1}],
[],
{}
]
"""

text1 = aocd.get_data(day=day, year=year)


def get_numbers(o, part_one):
    if isinstance(o, str):
        if o.isnumeric():
            return [int(o)]

    if isinstance(o, int):
        return [o]

    l = []
    if isinstance(o, dict):
        if part_one or not 'red' in o.values():
            for i in o.values():
                l += get_numbers(i, part_one)

    if isinstance(o, list):
        for i in o:
            l += get_numbers(i, part_one)

    return l


if __name__ == '__main__':
    text = text1
    text = json.loads(text)

    pone = sum(get_numbers(text, True))
    ptwo = sum(get_numbers(text, False))


    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
