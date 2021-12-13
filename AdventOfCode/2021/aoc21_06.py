# Advent of Code 2021
# Day 6

import numpy as np
import aocd

text0 = "3,4,3,1,2"
text1 = aocd.get_data(day=6, year=2021)


def sim_life(fish, days):
    for i in range(days):
        n = fish[0]
        fish[:-1] = fish[1:]
        fish[6] += n
        fish[8] = n
    return fish


if __name__ == "__main__":
    text = text1

    fish0 = np.zeros(9, dtype=np.int64)
    for t in text.split(","):
        fish0[int(t)] += 1

    fish = sim_life(fish0.copy(), 80)
    print(f"Part one: {fish.sum()}")

    fish = sim_life(fish0.copy(), 256)
    print(f"Part one: {fish.sum()}")

