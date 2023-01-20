# Advent of Code
year = 2017
day = 6

import numpy as np
import aocd

text0 = """0 2 7 0"""
text1 = aocd.get_data(day=day, year=year)

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().split()

    arr = np.array([int(c) for c in text])

    n, r = 0, 0
    s = [tuple(arr)]
    while True:
        print(len(s), arr)
        i = arr.argmax()
        n = arr[i]
        arr[i] = 0
        arr += n // len(arr)
        n = n % len(arr)
        if n == 0:
            pass
        elif n + i < len(arr):
            arr[i+1:i+1+n] += 1
        else:
            arr[i+1:] += 1
            arr[:(i+1+n)%len(arr)] += 1
        t = tuple(arr)
        if t in s:
            break
        s.append(t)

    pone = len(s)
    ptwo = len(s) - s.index(t)

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
