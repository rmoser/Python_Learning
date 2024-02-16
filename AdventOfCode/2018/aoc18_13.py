# Advent of Code
year = 2018
day = 13

import numpy as np
import aocd

text0 = r"""
/->-\        
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   
"""

text0 = r"""
/>-<\  
|   |  
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/
"""
text1 = aocd.get_data(day=day, year=year)


def turn(c, s):
    dirs = ['>', 'v', '<', '^']
    i = dirs.index(c)
    if s == 0:    # Left
        i = (i - 1) % 4
    elif s == 2:  # Right
        i = (i + 1) % 4
    return dirs[i]


def show(board, carts=None):
    for y in range(len(board)):
        for x in range(len(board[0])):
            if carts and (x, y) in carts:
                print(carts[x, y][0], end='')
            else:
                print(board[y][x], end='')
        print()


def run(board, carts, n=np.inf):
    first = None
    final = None

    while n > 0:
        # show(board, carts)
        # new_carts = dict()
        for cart in sorted(carts):
            # In case cart was deleted due to a crash
            if not cart in carts:
                continue

            x, y = cart
            c, s = carts.pop(cart)

            if c == '>':
                x += 1
            elif c == 'v':
                y += 1
            elif c == '<':
                x -= 1
            elif c == '^':
                y -= 1

            if board[y][x] == '/':
                if c == '>':
                    c = '^'
                elif c == 'v':
                    c = '<'
                elif c == '<':
                    c = 'v'
                elif c == '^':
                    c = '>'

            elif board[y][x] == '\\':
                if c == '<':
                    c = '^'
                elif c == 'v':
                    c = '>'
                elif c == '>':
                    c = 'v'
                elif c == '^':
                    c = '<'

            elif board[y][x] == '+':
                c = turn(c, s)
                s = (s + 1) % 3

            if (x, y) in carts:
                if not first:
                    first = x, y
                carts.pop((x, y))
                continue

            # new_carts[x, y] = [c, s]
            carts[x, y] = [c, s]

            # print(carts)

        n -= 1

        if len(carts) == 1:
            final = list(carts.keys())[0]
            break

    return carts, first, final


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip('\n')
    if '\n' in text:
        text = text.splitlines()

    board = [list(x) for x in text]

    carts = dict()
    height = len(text)
    width = len(text[0])

    for x in range(width):
        for y in range(height):
            if board[y][x] in '><^v':
                c = board[y][x]
                carts[(x, y)] = [c, 0]
                if c in '<>':
                    board[y][x] = '-'
                elif c in 'v^':
                    board[y][x] = '|'

    carts, first, final = run(board, carts)

    pone = first
    print(f"AOC {year} day {day}  Part One: {pone}")

    ptwo = final
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
