# Advent of Code
year = 2024
day = 15

import numpy as np
import aocd
import os
import utils
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
    'v': np.array([1, 0])
}

def move(pos, arr, direction):
    d = DIRS[direction]
    new_pos = tuple(pos + d)

    # new pos is empty
    if array[new_pos] == '.':
        array[pos] = '.'
        array[new_pos] = '@'
        return new_pos

    # new pos is box:
    if array[new_pos] == 'O':
        new_pos2 = new_pos
        i = 1
        while array[new_pos2] == 'O':
            i += 1
            new_pos2 = tuple(new_pos2 + d)

        # Space to move box:
        if array[new_pos2] == '.':
            array[new_pos2] = 'O'
            array[new_pos] = '@'
            array[pos] = '.'
            return new_pos

    return pos


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip()

    a, b = text.split('\n\n')
    array = np.array([list(x) for x in a.splitlines()])

    instructions = ''.join(list(b.splitlines()))

    pos = tuple(np.array(np.where(array == '@')).flatten().tolist())

    for i in list(instructions):
        pos = move(pos, array, i)


    utils.show(array, translate=False)

    pone = (np.array(np.where(array == 'O')) * [[100], [1]]).sum()

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
