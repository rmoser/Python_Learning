# Advent of Code
year = 2024
day = 13

import numpy as np
import aocd
import os
# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

text0 = """
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""
text1 = aocd.get_data(day=day, year=year)

def play(machine, offset=0):
    a, b, prize = tuple(np.array(x) for x in machine)
    prize += offset
    ans = np.linalg.solve(np.array([a, b]).T, np.array([prize]).T).flatten().round(1).astype(int)
    if ((ans * np.array([a, b]).T).sum(axis=1) == prize).all():
        return ans.astype(int).tolist()
    return 0, 0

def play_brute(machine, offset=0):
    a, b, prize = tuple(np.array(x, dtype=int) for x in machine)
    prize += offset

    # A x + B y = C
    # D x + E y = F
    # x = (C / B - F / E) / (A / B - D / E)
    a_count = int(((prize[0]/b[0]-prize[1]/b[1]) / (a[0]/b[0]-a[1]/b[1])).round(1))
    b_count = int(((prize[0]-a[0]*a_count)/b[0]).round(1))
    # print(a_count, b_count)
    if (a * a_count + b * b_count == prize).all():
        return a_count, b_count

    return 0, 0

if __name__ == '__main__':
    pone = 0
    ptwo = 0

    text = text1
    text = text.strip().splitlines()

    machines = []
    machine = []
    for line in text:
        if not line:
            continue
        name, xy = line.split(': ')
        x, y = xy.split(', ')
        x = int(x[2:])
        y = int(y[2:])
        machine.append((x, y))
        if len(machine) == 3:
            machines.append(machine)
            machine = []

    for machine in machines:
        a, b = play(machine)
        score = 3 * a + b
        pone += score
        # print(machine, a, b, score)

        a, b = play(machine, offset=10000000000000)
        score = 3 * a + b
        ptwo += score
        # a, b = play_brute(machine)
        # score_b = 3 * a + b
        # if score != score_b:
        #     print("!", machine, a, b, score_b)

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
