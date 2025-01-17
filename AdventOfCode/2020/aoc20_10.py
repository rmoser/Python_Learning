# Advent of Code
import typing

year = 2020
day = 10

import numpy as np
import numpy.typing as npt
import aocd
import os
from pprint import pprint
import itertools as it
import utils
import functools
import math

# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

text0 = """
16
10
15
5
1
11
7
19
6
12
4
"""
text1 = aocd.get_data(day=day, year=year)

def valid(adapters: (tuple, np.ndarray)):
    if not len(adapters) >= 2:
        return False
    if not isinstance(adapters, np.ndarray):
        adapters = np.array(adapters)
    deltas = adapters[1:] - adapters[:-1]
    return 0 <= deltas.max() <= 3

def to_byte(arr):
    if len(arr) > 64:
        return to_byte(arr[:-64]), to_byte(arr[-64:])
    return sum(int(x)*2**i for i, x in enumerate(arr[::-1]))

def to_arr(num: (int, tuple)):
    if isinstance(num, tuple):
        a = to_arr(num[0])
        if isinstance(a, np.ndarray):
            return np.concatenate((a, to_arr(num[1])))
        else:
            return a + to_arr(num[1])
    return np.array([x=='1' for x in bin(num)[2:]])

def subsets(adapters):
    a = np.array(adapters)
    delta_three = [-1] + np.where((a[1:] - a[:-1]) == 3)[0].tolist()
    return [adapters[a+1:b+1] for a, b in it.pairwise(delta_three)]

def valid_iter(adapters: (tuple, np.ndarray)):
    n = len(adapters)
    if n == 1:
        return 1

    count = 0
    if valid(adapters):
        count = 1
    stack = [2**n-1]

    for i in range(1, n-1):
        for s in range(len(stack)):
            mask = to_arr(stack[s])
            mask[i] = 0
            adapter = tuple(it.compress(adapters, mask))
            if valid(adapter):
                stack.append(to_byte(mask))
                count += 1

    return count

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()
    adapters = list(sorted(int(x) for x in text))
    adapters = np.array([0] + adapters + [max(adapters) + 3])

    deltas = adapters[1:] - adapters[:-1]
    pone = sum(deltas == 1) * sum(deltas == 3)

    print(f"AOC {year} day {day}  Part One: {pone}")

    adapter_subsets = subsets(adapters)
    ptwo = math.prod(valid_iter(a) for a in adapter_subsets)


    print(f"AOC {year} day {day}  Part Two: {ptwo}")
