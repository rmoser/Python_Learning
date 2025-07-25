# Advent of Code
year = 2023
day = 10

import numpy as np
import aocd
import utils


text0 = """
.....
.S-7.
.|.|.
.L-J.
.....
"""
text1 = aocd.get_data(day=day, year=year)


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()
    area = np.array([[c for c in line] for line in text])
    start = tuple(np.asarray(np.where(area=='S')).T.flatten())
    pos = start
    DIRS = np.array(((0, 1), (1, 0), (0, -1), (-1, 0)))

    path = [start]
    while True:
        # Down
        if pos[0] < area.shape[0] and (area[pos] in '|7F' or area[pos] == 'S'):
            _pos = (pos[0]+1, pos[1])
            if area[_pos] == 'S':
                break
            if area[_pos] in '|JL' and _pos not in path:
                pos = _pos
                path.append(_pos)
                continue
        # Up
        if pos[0] > 0 and (area[pos] in '|LJ' or area[pos] == 'S'):
            _pos = (pos[0]-1, pos[1])
            if area[_pos] == 'S':
                break
            if area[_pos] in '|7F' and _pos not in path:
                pos = _pos
                path.append(_pos)
                continue

        # Left
        if pos[1] > 0 and (area[pos] in '-7J' or area[pos] == 'S'):
            _pos = (pos[0], pos[1]-1)
            if area[_pos] == 'S':
                break
            if area[_pos] in '-LF' and  _pos not in path:
                pos = _pos
                path.append(_pos)
                continue

        # Right
        if pos[1] < area.shape[1] and (area[pos] in '-FL' or area[pos] == 'S'):
            _pos = (pos[0], pos[1]+1)
            if area[_pos] == 'S':
                break
            if area[_pos] in '-J7' and  _pos not in path:
                pos = _pos
                path.append(_pos)
                continue

    arr = (area != '.').astype(int)

    path.append(path[0])

    for i in range((len(path) + 1) // 2):
        arr[path[i]] = i
        arr[path[-i-1]] = i

    pone = arr.max()

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
