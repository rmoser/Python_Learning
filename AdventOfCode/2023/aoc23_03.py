# Advent of Code
year = 2023
day = 3

import numpy as np
import scipy as sp
import aocd
import itertools as it
from pprint import pprint
import functools
import math

text0 = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""
text1 = aocd.get_data(day=day, year=year)

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    arr = np.array([list(x) for x in text])

    symbols = np.where(np.bitwise_not(np.isin(arr, list('0123456789.'))))  # Symbol positions
    symbol_positions = tuple(map(tuple, np.array(symbols).T.tolist()))
    nums = np.where(np.char.isnumeric(arr))
    num_positions = tuple(map(tuple, np.array(nums).T.tolist()))
    # nums_c = list(map(tuple, np.matrix(nums).T.tolist()))
    # nums_c = np.matrix(nums).T

    ones = np.ones(shape=(len(symbols[0]), 1), dtype=int)
    symbol_adjacency = np.bitwise_and(np.abs(nums[0] * ones - np.expand_dims(symbols[0], axis=1)) < 2, np.abs(nums[1] * ones - np.expand_dims(symbols[1], axis=1)) < 2).astype(int)

    ones = np.ones(shape=(len(nums[0]), 1), dtype=int)
    num_adjacency = np.bitwise_and(np.abs(nums[0] * ones - np.expand_dims(nums[0], axis=1)) == 0, np.abs(nums[1] * ones - np.expand_dims(nums[1], axis=1)) == 1).astype(int)
    np.fill_diagonal(num_adjacency, 0)

    nums_collated = []
    for i in range(len(num_positions)):
        if i==0 or not num_adjacency[i, i-1]:
            nums_collated.append({i})

        if i > 0 and num_adjacency[i, i-1]:
            nums_collated[-1].add(i-1)
            nums_collated[-1].add(i)
        if i+1 < len(num_positions) and num_adjacency[i, i+1]:
            nums_collated[-1].add(i+1)
            # print(nums_collated[-1])

    nums = dict()
    for num_ids in nums_collated:
        if not num_ids:
            continue
        symbol_adjacent = max(symbol_adjacency[:, n].any() for n in num_ids)

        value = int(''.join([arr[num_positions[n]] for n in sorted(num_ids)]))
        pos = tuple(sorted(num_positions[n] for n in num_ids))
        # nums[pos] = (value, symbol_adjacent)
        if not value in nums:
            nums[value] = [0, []]

        if symbol_adjacent:
            nums[value][0] += 1
        nums[value][1].append(pos)


    @functools.cache
    def get_num(pos):
        # i = num_positions.index(pos)
        for k, v in nums.items():
            for pos_list in v[1]:
                if pos in pos_list:
                    return k, pos_list


    symbols = dict()
    for i, pos in enumerate(symbol_positions):
        symbol = arr[pos]
        if symbol != '*':
            continue
        pos_list = [x[0] for x in zip(num_positions, symbol_adjacency[i]) if x[1]]
        symbols[i] = set(get_num(x) for x in pos_list)


    pone = sum(k * v[0] for k, v in nums.items())
    print(f"AOC {year} day {day}  Part One: {pone}")

    ptwo = sum(math.prod(x[0] for x in v) for k,v in symbols.items() if len(v) == 2)
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
