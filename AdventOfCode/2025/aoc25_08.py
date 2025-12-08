# Advent of Code
from scipy.spatial import distance_matrix

year = 2025
day = 8

import numpy as np
import scipy as sp
import aocd
import os
import utils
from pprint import pprint
from icecream import ic
import itertools as it

text0 = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
"""
text1 = aocd.get_data(day=day, year=year)

def circuits(arr, n=None):
    circuit = []
    data = {}

    def connect(a, b):
        a = int(a)
        b = int(b)

        # if a in data and b in data:
        #     circuit_a = data[a]
        #     circuit_b = data[b]
        #     circuit_a |= circuit_b
        #     circuit.remove(circuit_b)

        ic(data)
        ic(circuit)

        if a in data:
            circuit_a = data[a]
            ic(f'Found {a} in {circuit_a}')
        else:
            circuit_a = {a}
            data[a] = circuit_a
            ic(f'New {a} in {circuit_a}')

        if b in data:
            circuit_b = data[b]
            ic(f'Found {b} in {circuit_b}')
        else:
            circuit_b = {b}
            ic(f'New {b} in {circuit_b}')

        if circuit_a is circuit_b:
            ic(f'{a} already connected to {b}: {circuit_a}')
            return

        for node in circuit_b:
            data[node] = circuit_a

        circuit_a |= circuit_b
        ic(f'Extended circuit_a: {circuit_a}')

        if circuit_a not in circuit:
            circuit.append(circuit_a)
            ic(f"Appended {circuit_a} to {circuit}")
        if circuit_b in circuit:
            circuit.remove(circuit_b)
            ic(f"Removed {circuit_b} from {circuit}")


    if n is None:
        n = arr.shape[0]

    distance_matrix = np.full((arr.shape[0], arr.shape[0]), fill_value=np.inf)

    for a, b in it.combinations(range(arr.shape[0]), 2):
        distance_matrix[a, b] = sp.spatial.distance.euclidean(arr[a], arr[b])

    for _ in range(n):
        a, b = divmod(distance_matrix.argmin(), arr.shape[0])
        connect(a, b)
        distance_matrix[a, b] = np.inf

    return circuit

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    _text = text.strip().splitlines()

    ic.disable()

    arr = np.array([[int(x) for x in line.split(',')] for line in _text])
    c = circuits(arr, 10 if text == text0 else None)
    lens = np.array([len(x) for x in c])
    lens.sort()
    pone = lens[-3:].prod()

    ic(c)


    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
