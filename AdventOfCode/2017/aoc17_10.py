# Advent of Code
year = 2017
day = 10

import numpy as np
import aocd
import itertools

text0 = """3,4,1,5"""
text2 = ""
text1 = aocd.get_data(day=day, year=year)


def ravel(arr, i, n):
    if n == 1:
        return arr

    arr = arr.copy()

    if i >= len(arr):
        i = i % len(arr)

    # Rotate left by i
    arr = arr[i:] + arr[:i]

    # Reverse n elements
    arr[:n] = arr[:n][::-1]

    # Rotate right by i
    return arr[len(arr)-i:] + arr[:len(arr)-i]


def knot(arr, inst, i=0, skip=0, repeat=1):
    # print(' ', i, skip, arr)
    for _ in range(repeat):
        for n in inst.copy():
            arr = ravel(arr, i, n)
            i = (i + n + skip) % len(arr)
            skip += 1
            # print(n, i, skip, arr)
    return arr, i, skip


def xor(arr):
    from functools import reduce
    return [reduce(lambda x, y: x ^ y, arr[i:i+16]) for i in range(0, len(arr), 16)]


def ascii(arr):
    return ''.join(format(x, 'X').rjust(2, '0') for x in arr)


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    if text == text0:
        arr = list(range(5))
    else:
        arr = list(range(256))

    inst = text.strip()
    inst = [int(c) for c in inst.split(',')]


    # skip = 0
    # i = 0
    # print(' ', i, skip, arr)
    # for n in text:
    #     arr = ravel(arr, i, n)
    #     i = (i + n + skip) % len(arr)
    #     skip += 1
    #     print(n, i, skip, arr)

    arr, _, _ = knot(arr, inst)
    print(arr)
    pone = arr[0] * arr[1]

    print(f"AOC {year} day {day}  Part One: {pone}")

    arr = list(range(256))
    if text == text0:
        text = text2
    inst = [ord(c) for c in text] + [17, 31, 73, 47, 23]
    arr, _, _ = knot(arr, inst, repeat=64)
    ptwo = ascii(xor(arr)).lower()


    print(f"AOC {year} day {day}  Part Two: {ptwo}")
