# Advent of Code
year = 2019
day = 2

import numpy as np
import aocd

text0 = """1,9,10,3,2,3,11,0,99,30,40,50"""
text1 = aocd.get_data(day=day, year=year)


def intcode(arr):
    i = 0
    while arr[i] in (1, 2):
        # print(i, arr[i], arr)
        a = arr[arr[i + 1]]
        b = arr[arr[i + 2]]
        addr = arr[i + 3]

        if arr[i] == 1:
            arr[addr] = a + b
        elif arr[i] == 2:
            arr[addr] = a * b

        i += 4

    # print(arr)
    return arr[0]


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip()
    if '\n' in text:
        test = text.splitlines()

    arr = [int(x) for x in text.split(',')]
    arr[1] = 12
    arr[2] = 2

    pone = intcode(arr)

    print(f"AOC {year} day {day}  Part One: {pone}")

    ans = 19690720

    result = 0
    v = 0

    for n in range(1000):
        arr = [int(x) for x in text.split(',')]
        arr[1:3] = [n, v]
        result = intcode(arr)

        print(n, v, result)
        if result > ans:
            n -= 1
            break

    for v in range(1000):
        arr = [int(x) for x in text.split(',')]
        arr[1:3] = [n, v]
        result = intcode(arr)

        print(n, v, result)
        if result == ans:
            break

    ptwo = 100 * n + v
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
