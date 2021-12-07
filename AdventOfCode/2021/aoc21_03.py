# Advent of Code 2021
# Day 3

import numpy as np

import numpy as np
import aocd
day = 3
text1 = aocd.get_data(day=day, year=2021)


text0 = '''
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
'''

text = text1

data = np.asarray(list(map(list, text.split())))
data = data.astype(bool)
bits = (data.mean(axis=0) * 2).astype(int).astype(bool)
gamma = sum(e*2**i for i, e in enumerate(bits[::-1]) if e)
epsilon = sum(2**i for i, e in enumerate(np.bitwise_not(bits)[::-1]) if e)
print(f"bits: {bits}:  gamma: {gamma}  epsilon: {epsilon}")
print(f"Part one result: {gamma * epsilon}")


# Part Two
data0 = data.copy()

for i in range(data0.shape[1]):
    mode = ((data0[:, i]).mean() * 2).astype(int)
    if mode > 1:
        mode = 1
    data0 = data0[data0[:, i] == mode, :]
    print(f"iter: {i}, mode: {mode}\n{data0}")
    if len(data0) == 1:
        break

o2 = sum(e * 2 ** i for i, e in enumerate(data0[0][::-1]) if e)


data0 = data.copy()

for i in range(data0.shape[1]):
    mode = ((data0[:, i]).mean() * 2).astype(int)
    if mode > 1:
        mode = 1
    data0 = data0[data0[:, i] != mode, :]
    print(f"iter: {i}, mode: {mode}\n{data0}")
    if len(data0) == 1:
        break

co2 = sum(e * 2 ** i for i, e in enumerate(data0[0][::-1]) if e)

print(f"o2: {o2}, co2: {co2}")
print(f"Part two result: {o2 * co2}")



