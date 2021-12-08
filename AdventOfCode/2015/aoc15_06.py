# Advent of Code
year = 2015
day = 6

import numpy as np
import aocd

text0 = "turn on 0,0 through 999,999"
text1 = aocd.get_data(day=day, year=year)


if __name__ == '__main__':
    text = text1

    text = text.splitlines()

    grid = np.zeros((1000, 1000), bool)

    for cmd in text:
        command = cmd.split()
        corners = np.array([command[-3].split(","), command[-1].split(",")]).flatten().astype(int)
        # print(f"cmd: {command} -> corners {corners}")

        x0, y0, x1, y1 = corners
        x1 += 1
        y1 += 1

        # print(grid[x0:x1, y0:y1])

        if command[0] == 'toggle':
            grid[x0:x1, y0:y1] = np.bitwise_not(grid[x0:x1, y0:y1])
        elif command[1] == 'on':
            grid[x0:x1, y0:y1] = True
        elif command[1] == 'off':
            grid[x0:x1, y0:y1] = False

        # print(grid[x0:x1, y0:y1])

    print(f"AOC {year} day {day}  Part One: {grid.sum()}")


    grid = np.zeros((1000, 1000), int)

    for cmd in text:
        command = cmd.split()
        corners = np.array([command[-3].split(","), command[-1].split(",")]).flatten().astype(int)
        # print(f"cmd: {command} -> corners {corners}")

        x0, y0, x1, y1 = corners
        x1 += 1
        y1 += 1

        # print(grid[x0:x1, y0:y1])

        if command[0] == 'toggle':
            grid[x0:x1, y0:y1] += 2
        elif command[1] == 'on':
            grid[x0:x1, y0:y1] += 1
        elif command[1] == 'off':
            grid[x0:x1, y0:y1] -= 1
            grid[grid < 0] = 0

    print(f"AOC {year} day {day}  Part Two: {grid.sum()}")
