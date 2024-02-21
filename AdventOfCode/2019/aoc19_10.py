# Advent of Code
year = 2019
day = 10

import numpy as np
import aocd
import math
import itertools

text0 = """
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
"""
text1 = aocd.get_data(day=day, year=year)

GCD_COORDS = dict()


def gcd_coords(a, b):
    if a == b:
        return

    y, x = a

    d_y = b[0] - a[0]
    d_x = b[1] - a[1]
    ad_x = abs(d_x)
    ad_y = abs(d_y)
    if (d_y, d_x) in GCD_COORDS:
        ans = set((a[0] + _y, a[1] + _x) for _y, _x in GCD_COORDS[d_y, d_x])
        return ans

    # if bool(ad_x) and bool(ad_y):
    g = math.gcd(ad_y, ad_x)
    _y = d_y // g
    _x = d_x // g
    # else:
    #     _x = bool(ad_x)
    #     _y = bool(ad_y)

    if _x:
        r = range(1, d_x // _x)
        # if d_x < 0:
        #     r = [-1 * j for j in r]
    elif _y:
        r = range(1, d_y // _y)
        # if d_y < 0:
        #     r = [-1 * j for j in r]

    _ans = set((i * _y, i * _x) for i in r)
    GCD_COORDS[d_y, d_x] = _ans
    ans = set((a[0] + _y, a[1] + _x) for _y, _x in _ans)
    return ans


def gcd_coords_all(arr):
    if isinstance(arr, list):
        coords = arr
    else:
        coords = np.indices(arr.shape).transpose((2, 1, 0)).reshape(np.prod(arr.shape), 2)
    for a, b in itertools.combinations(coords, 2):
        z = gcd_coords(tuple(a), tuple(b))


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text0
    text = text.strip()
    if '\n' in text:
        text = text.splitlines()
    arr = np.array([list(x) for x in text]) == '#'

    asteroids = list(zip(*np.where(arr)))
    gcd_coords_all(asteroids)

    ans = np.zeros_like(arr, dtype=int)
    # coords = np.indices(arr.shape).transpose((2,1,0)).reshape(np.prod(arr.shape), 2)
    for i in range(len(asteroids)-1):
        a = asteroids[i]
        x = asteroids[i+1:]
        for b in x:
            # print(a, b)
            c = gcd_coords(a, b)
            if c:
                # c = np.array(list(x))
                if any(list(arr[tuple(_c)] for _c in c)):
                    continue
            # print("YES")
            ans[a] += 1
            ans[b] += 1
        # print(f"{i} {a} < {x}\n", ans)

    pone = ans.max()
    print(f"AOC {year} day {day}  Part One: {pone}")

    station = np.unravel_index(ans.argmax(), ans.shape)
    asteroids.remove(station)
    vaporized = []
    angles = [math.atan2(station[0]-y, x-station[1]) for y, x in asteroids]
    angles = [math.pi / 2 - a for a in angles]  # Convert to polar with 0 as up
    distances = [math.sqrt((station[0]-y)**2 + (station[1]-x)**2) for x, y in asteroids]
    polar_sorted = dict()
    for asteroid, angle, distance in zip(asteroids, angles, distances):
        if not angle in polar_sorted:
            polar_sorted[angle] = []
        polar_sorted[angle] = sorted(polar_sorted[angle] + [(distance, asteroid)])

    angles = sorted(polar_sorted.keys())

    # Rotate to start at 0
    i = angles.index(0.0)
    angles = angles[i:] + angles[:i]

    while len(vaporized) < 200:
        for angle in angles:
            for pos in polar_sorted[angle]:
                if gcd_coords(station, pos):
                    continue
                vaporized.append(pos)
                polar_sorted[angle].remove(pos)


    ptwo = 100 * vaporized[200][1] + vaporized[200][0]
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
