# Advent of Code
year = 2016
day = 17

import numpy as np
import aocd
import hashlib
import itertools

text0 = """ihgpwlah"""
text1 = aocd.get_data(day=day, year=year)


def md5(text):
    return hashlib.md5(text.encode()).hexdigest()


def moves(text):
    return ['UDLR'[i] for i in range(4) if text[i] in 'bcdef']


def valid_path(maze, start, end, paths=None, iters=-1, debug=False, find_all=False):
    debug = False
    moves_pos = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}
    done = []

    if not paths:
        paths = ['']

    while True:
        if len(paths) == 0:
            print()
            return done
        max_len = max(len(x) for x in paths)

        print(f'\riter: {iters}  paths: {len(paths)}  done: {len(done)}  max: {max_len}', end='')

        for _ in range(len(paths)):
            path = paths.pop(0)
            if len(path) == 0:
                pos = np.array(start)
            else:
                pos = np.array([moves_pos[c] for c in path]).sum(axis=0)

            for move in moves(md5(maze + path)):
                new_path = path + move

                new_pos = pos + moves_pos[move]

                # Check if new position is within the maze
                if (new_pos < 0).any() or (new_pos > 3).any():
                    continue

                # Check if we reached the exit
                if (new_pos == (3, 3)).all():
                    done.append(new_path)
                    if debug:
                        print("Done! ", move, new_path)
                    if not find_all:
                        return done
                    continue

                paths.append(new_path)
                if debug:
                    print("Path stub: ", path, move)

        if debug:
            print('\n Paths: ', paths)

        iters -= 1
        if iters == 0:
            return done, paths


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip()

    m = md5(text + 'D')
    # print(m[:4], moves(m))

    all_paths = valid_path(text, (0, 0), (3, 3), find_all=True)

    pone = all_paths[0]
    print(f"AOC {year} day {day}  Part One: {pone}")

    ptwo = len(all_paths[-1])
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
