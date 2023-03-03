# Advent of Code
year = 2022
day = 13

import numpy as np
import aocd
from itertools import zip_longest
from functools import cmp_to_key
from math import prod

text0 = """
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
"""
text1 = aocd.get_data(day=day, year=year)


def compare(left, right):
    if left is None:
        return -1
    if right is None:
        return 1

    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return -1
        if left > right:
            return 1
        return 0

    if isinstance(left, int):
        left = [left]
    if isinstance(right, int):
        right = [right]

    for l, r in zip_longest(left, right):
        if (result := compare(l, r)) != 0:
            return result
    return 0


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    a_list = []
    b_list = []
    a = None
    for line in text:
        if not line:
            continue

        if a is None:
            a = eval(line)
            continue

        a_list.append(a)
        b = eval(line)
        b_list.append(b)
        # print(line, a, b)
        a = None

    # print(a_list, b_list)

    items = list(zip(a_list, b_list))

    # for i, item in enumerate(items):
    #     if (compare(*item) == -1) != in_order(*item):
    #         print(i+1, item[0], "   <--->   ", item[1])
    #         print(f"\tCompare: {compare(*item)}")
    #         print(f"\tInOrder: {in_order(*item)}")

    pone = sum([i+1 for i, item in enumerate(items) if compare(*item) == -1])

    print(f"AOC {year} day {day}  Part One: {pone}")

    ptwo_list = a_list + b_list + [[[2]], [[6]]]

    ptwo_list.sort(key=cmp_to_key(compare))

    ptwo = prod([i+1 for i, item in enumerate(ptwo_list) if item in ([[2]], [[6]])])
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
