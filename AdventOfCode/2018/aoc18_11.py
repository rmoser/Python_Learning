# Advent of Code
year = 2018
day = 11

import numpy as np
import aocd
import re

text0 = """18"""
text1 = aocd.get_data(day=day, year=year)


def power(c, sn):
    rack_id = c[0] + 10
    p = rack_id * c[1]
    p += sn
    p *= rack_id
    p //= 100
    p %= 10
    p -= 5
    return p


def max_power(arr, size=3):
    p = np.zeros(shape=(300-size, 300-size), dtype=int)
    for x in range(0, 300-size):
        for y in range(0, 300-size):
            p[(x,y)] = arr[x:x+size,y:y+size].sum()
    return p


def max_power2(arr):
    p = np.zeros(shape=(300, 300, 300), dtype=int)
    for s in range(1, 300):
        for x in range(300-s):
            for y in range(300-s):
                p[(x,y,s)] = arr[x:x+s, y:y+s].sum()
    return p


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip()
    if '\n' in text:
        text = text.splitlines()

    text = int(text)

    arr = np.zeros(shape=(300, 300), dtype=int)
    for x in range(300):
        for y in range(300):
            arr[x, y] = power((x, y), text)

    m = max_power(arr)
    a = m.argmax()
    x = a // 297
    y = a % 297

    pone = f"{x},{y}"

    print(f"AOC {year} day {day}  Part One: {pone}")

    # p = max_power2(arr)

    recipes = [((0, 0), 0)]
    for i in range(1, 300):
        m = max_power(arr, i)
        a = m.argmax()
        x = a // (300 - i)
        y = a % (300 - i)
        recipes.append(((x, y), m[(x, y)]))

    m = np.array([x[1] for x in recipes])
    a = m.argmax()
    x, y = recipes[a][0]
    ptwo = f"{x},{y},{a}"

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
