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

global arr, _x0, _y0, ymax


def show(a):
    for row in range(a.shape[0]):
        print('\0' + ''.join(a[row, :]))


def drop(s=None):
    x, y = s
    x -= _x0
    y -= _y0
    while y < ymax and arr[y+1, x] not in "~#":
        y += 1

    arr[s[1]-_y0+1:y+1, x] = '|'
    if y == ymax:
        return None
    else:
        return x+_x0, y+_y0


def flow(s):
    if not s:
        return []
    x, y = s
    x -= _x0
    y -= _y0

    l = x
    r = x
    _s = []  # New Sources to return
    while True:  # Search right
        if arr[y, r] == '#':
            break
        if arr[y+1, r] in '.|':
            arr[y, r] = '|'
            _s.append((r+_x0, y+_y0))
            break
        arr[y, r] = '|'
        r += 1

    while True:  # Search left
        if arr[y, l] == '#':
            break
        if arr[y+1, l] in '.|':
            arr[y, l] = '|'
            _s.append((l+_x0, y+_y0))
            break
        arr[y, l] = '|'
        l -= 1

    if arr[y, l] == '#' and arr[y, r] == '#':
        arr[y,l+1:r] = '~'
        return flow((x+_x0, y-1+_y0))

    return _s


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip()
    if '\n' in text:
        text = text.splitlines()

    sources = [(500, 0)]
    source = sources[0]
    sources = set(sources)

    insts = []
    xmin, xmax = source[0], source[0]
    ymin, ymax = np.inf, -np.inf
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

    arr = np.full(fill_value='.', shape=(ymax+1, xmax-xmin+3), dtype=str)
    _x0 = xmin - 1
    _y0 = 0
    arr[source[1]-_y0, source[0]-_x0] = '+'

    for x, y in insts:
        # print(x, y)
        for _x in x:
            for _y in y:
                arr[_y-_y0, _x-_x0] = '#'

    show(arr)

    while sources:
        print(f"\rSources: {len(sources)}, {sources}")
        s = sources.pop()

        for _s in flow(drop(s)):
            sources.add(_s)
        # print(sources)

    # print()
    show(arr)

    pone = np.bitwise_or(arr[ymin:ymax+1,:] == '|', arr[ymin:ymax+1,:] == '~').sum()
    print(f"AOC {year} day {day}  Part One: {pone}")

    ptwo = (arr[ymin:ymax+1,:] == '~').sum()
    print(f"AOC {year} day {day}  Part Two: {ptwo}")

