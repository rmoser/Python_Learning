# Advent of Code
year = 2024
day = 15

import numpy as np
import aocd
import os
import utils
import tkinter as tk
from collections import defaultdict

DEBUG = False

# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

text0 = """
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
"""
text1 = aocd.get_data(day=day, year=year)

DIRS = {
    '^': np.array([-1, 0]),
    '>': np.array([0, 1]),
    '<': np.array([0, -1]),
    'v': np.array([1, 0]),
}

def move(pos, array, direction):
    my_arr = array.copy()
    # pos must be indexable into array
    # either simple tuple (row, column)
    # or tuple of matched (rows, columns)

    d = DIRS[direction]
    new_pos = tuple((np.array(pos).T + d).T)

    # new pos is box:
    if np.array(array[new_pos] == 'O').all():
        # try to move the object out of the way
        move(new_pos, array, direction)

    multi_move = 0
    if np.bitwise_or(array[new_pos] == '[', array[new_pos] == ']').any():
        if direction in '<>':
            # try to move the object out of the way
            move(new_pos, array, direction)

        elif np.array(array[new_pos] == ['[', ']']).all():
            move(new_pos, array, direction)

        elif np.array(array[new_pos] == '[').all():
            _new_pos = (np.array([new_pos[0], new_pos[0]]), np.array([new_pos[1], new_pos[1]+1]))
            move(_new_pos, array, direction)

        elif np.array(array[new_pos] == ']').all():
            _new_pos = (np.array([new_pos[0], new_pos[0]]), np.array([new_pos[1]-1, new_pos[1]]))
            move(_new_pos, array, direction)

        else:
            # Try to move left object
            if array[new_pos[0][0], new_pos[1][0]] == ']':
                _new_pos = (np.array([new_pos[0][0], new_pos[0][0]]), np.array([new_pos[1][0]-1, new_pos[1][0]]))
                move(_new_pos, array, direction)

            # Try to move right object
            if array[new_pos[0][1], new_pos[1][1]] == '[':
                _new_pos = (np.array([new_pos[0][1], new_pos[0][1]]), np.array([new_pos[1][1], new_pos[1][1]+1]))
                move(_new_pos, array, direction)

    # now check if the move call made space
    # new pos is empty
    if np.array(array[new_pos]  == '.').all():
        array[new_pos] = array[pos]
        array[pos] = '.'
        return new_pos, array

    # Move failed
    return pos, my_arr


def textbox(message_text):
    root = tk.Tk()
    T = tk.Text(root, height=message_text.count('\n') + 3, width=len(message_text.split('\n')[0]) + 3)
    T.pack()
    T.insert(tk.END, message_text)
    tk.mainloop()


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip()

    a, b = text.split('\n\n')
    array = np.array([list(x) for x in a.splitlines()])
    array2 = np.zeros(shape=(array.shape * np.array([1, 2])), dtype=str)

    for c in range(array.shape[1]):
        col = np.zeros(shape=(array.shape[0], 2), dtype=str)
        # Copy to both columns
        col[:, 0] = array[:, c]
        col[:, 1] = array[:, c]

        # Parse objects and player
        col[col[:, 0] == 'O', 0] = '['
        col[col[:, 1] == 'O', 1] = ']'
        col[col[:, 1] == '@', 1] = '.'

        array2[:, c*2:c*2+2] = col

    instructions = ''.join(list(b.splitlines()))

    pos = tuple(np.array(np.where(array == '@')).flatten().tolist())
    pos2 = tuple(np.array(np.where(array2 == '@')).flatten().tolist())


    for i, d in enumerate(instructions):
        pos, array = move(pos, array, d)

        p = pos2
        _arr = array2.copy()
        pos2, array2 = move(pos2, array2, d)


    # utils.show(array, translate=False)
    # utils.show(array2, translate=False, start=pos2)

    pone = (np.array(np.where(array == 'O')) * [[100], [1]]).sum()
    ptwo = (np.array(np.where(array2 == '[')) * [[100], [1]]).sum()


    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
