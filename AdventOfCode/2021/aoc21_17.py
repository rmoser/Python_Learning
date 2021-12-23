# Advent of Code
year = 2021
day = 17

import numpy as np
import aocd

text0 = "target area: x=20..30, y=-10..-5"

text1 = aocd.get_data(day=day, year=year)


def path(v, target, n=None):
    p = [(0, 0)]
    velo = np.array(v)

    if n is None:
        n = -1

    y_tgt_min = min(target[:, 1])

    while True:
        n -= 1
        pos = tuple(p[-1] + velo)
        p.append(pos)
        velo = np.array([max(velo[0]-1, 0), velo[1]-1])

        if n == 0 or n < 0 and pos[1] < y_tgt_min:
            break

    return p


def valid_paths(target):
    result = []
    target_area = set(((x, y) for x in range(target[0, 0], target[1, 0]+1) for y in range(target[0, 1], target[1, 1]+1)))
    # print(target_area)
    x_tgt_min, x_tgt_max = target[:, 0]
    if x_tgt_min > 0:
        vx_min = 1
        vx_max = x_tgt_max
    elif x_tgt_max < 0:
        vx_max = -1
        vx_min = x_tgt_min
    else:
        vx_min = x_tgt_min
        vx_max = x_tgt_max

    y_tgt_min, y_tgt_max = target[:, 1]

    vy_min = min(1, y_tgt_min)
    if y_tgt_min > 0:
        vy_max = y_tgt_max
    elif y_tgt_max < 0:
        vy_max = abs(y_tgt_min)
    else:
        vy_max = 100

    # print('vx ', vx_min, vx_max)
    # print('vy ', vy_min, vy_max)

    i = 0
    for vx in range(vx_min, vx_max+1):
        for vy in range(vy_min, vy_max+1):
            i += 1
            # print(f"iter: {i} velo: ({vx}, {vy})")
            p = path((vx, vy), target)
            if set(p) & set(target_area):
                result.append(p)

    return result


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    _text = text.split(": ")[1].split(", ")
    target = np.array([tuple(x.split("=")[1].split("..")) for x in _text]).astype(int).T

    # print(target)
    # print(path((7, 2), target))

    paths = valid_paths(target)

    peak_ys = [max(c[1] for c in p) for p in paths]
    i_max = np.argmax(peak_ys)
    max_path = paths[i_max]

    pone = peak_ys[i_max]
    ptwo = len(paths)

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
