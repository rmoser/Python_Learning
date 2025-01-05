# Advent of Code
year = 2024
day = 22

import numpy as np
import aocd
import os
from pprint import pprint

# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

text0 = """
1
2
3
2024
"""

# text0 = """
# 123
# """
text1 = aocd.get_data(day=day, year=year)

def evolve(value: (int, np.ndarray), n: int = 1):
    x = value

    for _ in range(n):
        x = mix_prune(x, x * 64)
        x = mix_prune(x, x // 32)
        x = mix_prune(x, x * 2048)
    return x

def mix(a, b):
    return a ^ b

def prune(x):
    return x % 16777216

def mix_prune(a, b):
    return prune(mix(a, b))

def match(sequence, in_arr):
    n = len(sequence)
    m = np.zeros(shape=(in_arr.shape[0] - n + 1, n), dtype=int)
    for i in range(n):
        m[:, i] = np.array(in_arr[i:in_arr.shape[0]-n+i+1])

    return np.where((m == np.asarray(sequence)).all(axis=1))[0]


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = [int(x) for x in text.strip().splitlines()]

    max_n = len(text)
    arr = np.zeros(shape=(2001, max_n), dtype=int)
    arr[0] = text


    for r in range(1, 2001):
        arr[r] = list(map(evolve, arr[r-1]))

    pone = arr[-1].sum()

    print(f"AOC {year} day {day}  Part One: {pone}")


    _arr = arr % 10
    arr_delta = _arr[1:] - _arr[:-1]

    arr_delta_window = np.zeros(shape=[arr_delta.shape[0]-3, arr_delta.shape[1], 4], dtype=int)
    for i in range(4):
        arr_delta_window[:,:,i] = np.roll(arr_delta, -i, axis=0)[:-3]

    sequences = dict()
    for i in range(arr_delta_window.shape[1]):
        for s in set(tuple(x.tolist()) for x in arr_delta_window[:,i,:]):
            sequences[s] = sequences.get(s, 0) + 1

    sequences_ordered = dict()
    for s, v in sequences.items():
        if v not in sequences_ordered:
            sequences_ordered[v] = list()
        sequences_ordered[v].append(s)

    scores = dict()
    i = 0
    max_score = 0
    for n in range(max(sequences_ordered.keys()), -1, -1):
        if n not in sequences_ordered:
            continue
        if max_score >= 9 * n:
            print(f'\nMax score found.  Ending search...')
            break
        for s in sequences_ordered[n]:
            i += 1
            print(f'\r{n}: {i}/{len(sequences)}  max: {max_score}/{9*n}', end='\t\t\t\t\t\t\t')

            m = (arr_delta_window == s).all(axis=2)
            rows = np.argmax(m, axis=0) + 4
            anys = np.any(m, axis=0)
            scores[s] = (_arr[rows, np.arange(_arr.shape[1])] * anys).sum()
            max_score = max(max_score, scores[s])

    print()

    ptwo = max(scores.values())

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
