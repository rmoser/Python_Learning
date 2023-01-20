# Advent of Code
year = 2017
day = 3

import numpy as np
import aocd
import itertools

text0 = """
1024
"""

text1 = aocd.get_data(day=day, year=year)


def area(n):
    return (2*n+1) ** 2


def perimeter(n):
    if n == 0:
        return 1
    return area(n) - area(n-1)


def start(n):
    if n == 0:
        return 0, 0
    return 1-n, n


def get_ring(i):
    return (int((i-1) ** 0.5) + 1) // 2


def get_pos(i):
    if i == 1:
        return 0, 0

    ring = get_ring(i)
    p = perimeter(ring)
    d = i - area(ring-1)
    side_len = p // 4
    side_num, rem = divmod(d, side_len)

    pos = np.array(start(ring)) - (1, 0)  # Start counting from the corner

    # print(pos, side, rem, p//4)

    if side_num == 4:
        return tuple(pos)

    if side_num == 0:
        return tuple(pos + (rem, 0))

    pos += (side_len, 0)
    if side_num == 1:
        return tuple(pos - (0, rem))

    pos -= (0, side_len)
    if side_num == 2:
        return tuple(pos - (rem, 0))

    pos -= (side_len, 0)
    if side_num == 3:
        return tuple(pos + (0, rem))

    raise ValueError("No solution")


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip()

    text = int(text)

    pone = sum([abs(x) for x in get_pos(text)])
    print(f"AOC {year} day {day}  Part One: {pone}")

    r = get_ring(text)
    p = perimeter(r)
    s = p // 2 + 1

    arr = np.zeros((s, s), dtype=int)
    center = (1+s//2, 1+s//2)
    arr[center] = 1

    kernel = set(itertools.product([-1, 0, 1], repeat=2)) - {(0, 0)}
    kernel = np.array(list(kernel))

    for i in range(2, text):
        pos = tuple(np.array(center) + get_pos(i))
        k_pos = tuple((kernel + pos).T.tolist())
        arr[pos] = arr[k_pos].sum()

        if arr[pos] > text:
            ptwo = arr[pos]
            break

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
