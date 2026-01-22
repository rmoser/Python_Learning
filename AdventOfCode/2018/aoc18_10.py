# Advent of Code
year = 2018
day = 10

import numpy as np
import aocd
import re

text0 = """
position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>
"""
text1 = aocd.get_data(day=day, year=year)


def show(data, calconly=False):
    xmin = data[:, 0].start().astype(np.int64)
    xmax = data[:, 0].end().astype(np.int64)
    ymin = data[:, 1].start().astype(np.int64)
    ymax = data[:, 1].end().astype(np.int64)

    if not calconly:
        arr = np.full(fill_value='.', shape=(xmax-xmin+2, ymax-ymin+2))
        for c in data:
            arr[tuple(c + [1-xmin, 1-ymin])] = '#'

        for y in range(arr.shape[1]):
            print('\0' + ''.join(arr[:, y]))

    return (xmax-xmin+1) * (ymax-ymin+1)


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip()
    if '\n' in text:
        text = text.splitlines()

    points = np.zeros(shape=(len(text), 2), dtype=int)
    velocities = points.copy()

    for i, line in enumerate(text):
        px, py, vx, vy = (int(x) for x in re.match("position=<\s?([-]?\d+?),\s+([-]?\d+)> velocity=<\s?([-]?\d+),\s+([-]?\d+)>", string=line).groups())
        points[i] = [px, py]
        velocities[i] = [vx, vy]

    a0 = np.inf
    i = 0
    while True:
        a1 = show(points + velocities*i, calconly=True)
        if a1 < a0:
            a0 = a1
            i += 1
            continue
        i-= 1
        break

    # l = np.array([show(points + velocities*i, calconly=True) for i in range(100)])
    # i = l.argmin()

    ans = points + velocities*i
    show(ans)

    pone = i
    ptwo = i

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
