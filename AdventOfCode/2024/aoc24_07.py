# Advent of Code
year = 2024
day = 7

import numpy as np
import aocd
import os
# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

text0 = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""
text1 = aocd.get_data(day=day, year=year)

def check(ans, inputs, concat=False):
    if len(inputs) == 1:
        return ans == inputs[-1]
    if check(ans - inputs[-1], inputs[:-1], concat):
        return True
    if ans % inputs[-1] == 0 and check(ans // inputs[-1], inputs[:-1], concat):
        return True
    if concat and str(ans).endswith(str(inputs[-1])) and check(ans // (10 ** len(str(inputs[-1]))), inputs[:-1], concat):
        return True
    return False

if __name__ == '__main__':
    pone = 0
    ptwo = 0

    text = text1
    text = text.strip().splitlines()

    for line in text:
        ans, inputs = line.split(': ')
        ans = int(ans)
        inputs = [int(i) for i in inputs.split()]
        if check(ans, inputs):
            pone += ans
        if check(ans, inputs, concat=True):
            ptwo += ans

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
