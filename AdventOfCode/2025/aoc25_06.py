# Advent of Code
year = 2025
day = 6

import numpy as np
import aocd
import os
import utils
from pprint import pprint
from icecream import ic

text0 = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
"""
text1 = aocd.get_data(day=day, year=year)

def calc(data, ops):
    ans = 0
    for i in range(len(ops)):
        if ops[i] == '*':
            ans += data[:,i].prod()
        else:
            ans += data[:,i].sum()
    return ans

def convert(data):
    ans = np.zeros_like(data)
    for c in range(data.shape[1]):
        col_data = data[:,c]
        _data = np.array([list(x) for x in col_data])
        x = list(map(''.join, _data.T))
        ans[:len(x),c] = x
    return ans

def my_split(data):
    data = np.array([list(x) for x in data])
    for c in range(data.shape[1]):
        col_data = data[:,c]
        if (col_data == ' ').all():
            data[:,c] = ','
    data = np.array([(''.join(x).split(',')) for x in data])
    return data

if __name__ == '__main__':
    pone = ''
    ptwo = ''
    ic.disable()

    text = text1
    text = text.strip().splitlines()

    max_len = np.strings.str_len(text0.split()).max()
    data = my_split(text[:-1])
    ops = text[-1].split()
    ic(data)
    # ic(ops)

    pone = calc(data.astype(int), ops)
    print(f"AOC {year} day {day}  Part One: {pone}")

    converted = convert(data)
    for c in range(converted.shape[1]):
        converted[:,c][converted[:,c] == ''] = '1' if ops[c] == '*' else '0'

    ptwo = calc(converted.astype(int), ops)
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
