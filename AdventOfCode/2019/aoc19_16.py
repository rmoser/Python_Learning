# Advent of Code
year = 2019
day = 16

import numpy as np
import aocd
import pprint


text0 = """80871224585914546619083218645595"""
text0 = "12345678"
text1 = aocd.get_data(day=day, year=year)

def get_mul_arr(arr):
    pattern = np.array([0, 1, 0, -1], dtype=np.dtypes.Int8DType)
    len_arr = len(arr)
    _arr = np.empty((len_arr, len_arr), dtype=np.dtypes.Int8DType)
    for r in range(len_arr):
        _x = np.repeat(pattern, r+1)
        _pat = np.roll(_x, -1)
        n = len_arr // len(_pat) + 1
        _arr[r] = np.tile(_pat, n)[:len_arr]
        print("\rRow", r, "done.", end="")
    print()
    return _arr

def right_digit(n):
    return int(str(n)[-1])

# def get_mul(n=0, digit=0):
#     pattern = np.array([0, 1, 0, -1], dtype=int)
#     len_pattern = 4
#     return pattern[int((n+1)/(digit+1)) % len_pattern]

def run(arr):
    mul = get_mul_arr(arr)
    pprint.pprint(mul)

    new = np.empty_like(arr)
    for phase in range(100):
        for digit in range(len(arr)):
            new[digit] = right_digit((arr * mul[digit]).sum())
        #     a = [val * get_mul(i, digit) for i, val in enumerate(arr)]
        #     # print(phase, "a:", a)
        #     new[digit] = right_digit(sum(a))
        arr = new
        # new = np.vectorize(right_digit)((new * mul).sum(axis=1))
        print("\rPhase: ", phase, end="")
    print()
    return new

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text0
    text = text.strip()
    if '\n' in text:
        text = text.splitlines()

    arr = [int(x) for x in text]

    # print(arr)

    # Part One
    a = run(arr)
    pone = ''.join([str(x) for x in a[:8]])

    print(f"AOC {year} day {day}  Part One: {pone}")

    exit()

    # Part Two
    print("Creating data array")
    arr = np.array(arr, dtype=np.dtypes.Int8DType)
    arr = np.tile(arr, 10000)
    print("Creating mul array")

    print("Ready")

    offset = int(''.join((str(x) for x in arr[:7])))
    a = run(arr)
    ptwo = ''.join([str(x) for x in a[offset:offset+8]])


    print(f"AOC {year} day {day}  Part Two: {ptwo}")
