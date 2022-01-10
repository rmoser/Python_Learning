# Advent of Code
year = 2016
day = 18

import numpy as np
import aocd

text0 = ".^^.^.^^^^"
text1 = aocd.get_data(day=day, year=year)


def solve_text(maze, n):
    maze = [text]
    for j in range(n-1):
        print(f'\rrows {j+1}', end='')
        row = maze[-1]
        new_row = '^' if row[:2] in ('^^', '.^') else '.'
        for i in range(1, len(row)-1):
            new_row += '^' if row[i-1:i+2] in ('^^.', '.^^', '^..', '..^') else '.'
        new_row += '^' if row[-2:] in ('^^', '^.') else '.'
        maze.append(new_row)
    print()
    return maze


def solve_arr(maze, n):
    arr = np.zeros(shape=(n, len(maze)), dtype=np.bool)
    arr[0] = np.array(list(maze)) == '^'

    for row in range(1, n):
        subarr = np.pad(arr[row-1], (1, 1))
        l = subarr[:-2]
        c = subarr[1:-1]
        r = subarr[2:]
        c0 = l & c & np.logical_not(r)
        c1 = np.logical_not(l) & c & r
        c2 = l & np.logical_not(c) & np.logical_not(r)
        c3 = np.logical_not(l) & np.logical_not(c) & r
        arr[row] = c0 | c1 | c2 | c3

    return arr


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip()

    # maze = solve_text(text, 400000)
    maze = solve_arr(text, 400000)

    # pone = sum(x.count('.') for x in maze[:40)
    pone = np.logical_not(maze[:40]).sum()
    # _ = [print(x) for x in maze]

    # ptwo = sum(x.count('.') for x in maze)
    ptwo = np.logical_not(maze).sum()
    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
