# Advent of Code 2021
# Day 7

import numpy as np
import aocd

day = 7

text0 = "16,1,2,0,4,2,7,1,2,14"
text1 = aocd.get_data(day=day, year=2021)


def get_min_distance(arr, cost_f):
    mat = np.array([cost_f(arr-i) for i in np.arange(arr.max())])
    print(mat)
    dists = mat.sum(axis=1)
    idx = np.argsort(dists)[0]
    return idx, dists[idx]


def cost_func(d, pone=True):
    if pone:
        return abs(d)
    return np.round((d**2+abs(d))/2).astype(int)


if __name__ == '__main__':
    text = text1

    crabs = np.array(text.split(",")).astype(int)
    print(f"Part One:  Min Point and Distance: {get_min_distance(crabs, cost_func)}")

    print(f"Part Two:  Min Point and Distance: {get_min_distance(crabs, lambda x: cost_func(x, pone=False))}")





