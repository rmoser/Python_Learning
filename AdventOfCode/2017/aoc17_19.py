# Advent of Code
year = 2017
day = 19

import numpy as np
import aocd

text0 = r"""
     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+ 
                
"""
text1 = aocd.get_data(day=day, year=year)

if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    #text = text.strip()
    if '\n' in text:
        text = [x for x in text.splitlines() if x]
    arr = np.array([list(s) for s in text], dtype=str)

    pos = np.array((0, np.argwhere(arr[0] == '|')[0][0]), dtype=int)
    directions = {(0, 1), (0, -1), (1, 0), (-1, 0)}
    direction = (1, 0)

    letters = []
    steps = 0

    while ((0, 0) <= pos).all() and (pos < arr.shape).all() and arr[tuple(pos)] != ' ':
        steps += 1
        # print(pos)
        if arr[tuple(pos)].isalpha():
            letters += arr[tuple(pos)]
            pos += direction
            # print(pos, ''.join(letters))
            continue

        if arr[tuple(pos)] in ('-', '|'):
            pos += direction
            continue

        if arr[tuple(pos)] == '+':
            # print(pos)
            for d in directions - {direction} - {tuple(-np.array(direction))}:
                _pos = pos + d
                if ((0, 0) <= _pos).all() and (_pos < arr.shape).all():
                    if arr[tuple(_pos)] != ' ':
                        direction = d
                        pos = _pos
                        break

    pone = ''.join(letters)
    ptwo = steps

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
