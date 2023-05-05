# Advent of Code
year = 2018
day = 17

import numpy as np
import aocd
import utils

text0 = """
x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504
"""
text1 = aocd.get_data(day=day, year=year)


def show(a):
    for row in range(a.shape[0]):
        print(''.join(a[row, :]))


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text0
    text = text.strip()
    if '\n' in text:
        text = text.splitlines()

    source = (500, 0)

    insts = []
    xmin, xmax = source[0], source[0]
    ymin, ymax = source[1], source[1]
    for line in text:
        if not line:
            continue

        # print(line)
        a = line.split(', ')
        if line[0] == 'x':
            x = 0
            y = 1
        else:
            x = 1
            y = 0
        x = a[x]
        y = a[y]

        x = [int(i) for i in x.split('=')[1].split('..')]
        y = [int(i) for i in y.split('=')[1].split('..')]

        xmin = min([xmin] + x)
        xmax = max([xmax] + x)
        ymin = min([ymin] + y)
        ymax = max([ymax] + y)
        if len(x) > 1:
            insts.append((range(x[0], x[1]+1), y))
        else:
            insts.append((x, range(y[0], y[1]+1)))

    # print(xmin, xmax, ymin, ymax)

    arr = np.full(fill_value='.', shape=(ymax-ymin+1, xmax-xmin+3), dtype=str)
    _x0 = xmin - 1
    _y0 = ymin
    arr[source[1]-_y0, source[0]-_x0] = '+'

    for x, y in insts:
        # print(x, y)
        for _x in x:
            for _y in y:
                arr[_y-_y0, _x-_x0] = '#'

    show(arr)

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
