# Advent of Code
year = 2024
day = 16

import numpy as np
import aocd
import os
import utils
import functools
from pprint import pprint

# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

text00 = """
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
"""

text01 = """
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
"""

text1 = aocd.get_data(day=day, year=year)

DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
START_DIR = (0, 1)

@functools.cache
def score(path: tuple, direction: tuple = None):
    if len(path) == 1:
        if direction is None:
            return score(path, START_DIR)
        return 1000 * np.abs(np.array(direction) - START_DIR).max()

    if direction is None:
        return score(path, tuple((np.array(path[-1]) - path[-2]).tolist()))

    _direction = np.array(path[-1]) - path[-2]
    return score(path[:-1], tuple(_direction.tolist())) + 1 + 1000 * np.abs(direction - _direction).max()


def walk(maze, start, end, paths=None, iters=-1, debug=False):
    moves = np.array([(1, 0), (-1, 0), (0, 1), (0, -1)])
    if not paths:
        paths = [[start]]
    elif not isinstance(paths[0], list):
        paths = [paths]

    max_moves = np.prod(maze.shape)
    result_paths = []

    scores = dict()
    scores[start] = dict()
    for d in DIRS:
        scores[start][d] = score(tuple([start]), d)

    while paths:
        for _ in range(len(paths)):
            path = paths.pop(0)
            if len(path) >= max_moves:
                return []

            pos = path[-1]
            for move in moves:
                new_pos = pos + move  # type is np.array
                new_pos_tuple = tuple(new_pos.tolist())

                d = new_pos - pos
                d_tuple = tuple(d.tolist())

                if (new_pos < 0).any() or (new_pos >= maze.shape).any():
                    continue
                if new_pos_tuple in path:
                    # Circled back
                    continue
                if (new_pos == end).all():
                    result_paths.append(path + [new_pos_tuple])
                if maze[new_pos_tuple] == 0:
                    _path = path + [new_pos_tuple]
                    s = score(tuple(path), d_tuple)
                    if new_pos_tuple not in scores:
                        scores[new_pos_tuple] = dict()
                        for _d in DIRS:
                            scores[new_pos_tuple][_d] = score(tuple(path), _d)
                        scores[new_pos_tuple][d_tuple] = s

                    if s <= scores[new_pos_tuple][d_tuple]:
                        for _d in DIRS:
                            _s = score(tuple(_path), _d)
                            if _s < scores[new_pos_tuple][_d]:
                                scores[new_pos_tuple][_d] = _s
                        paths.append(_path)

                if debug:
                    print(move, path)

            if debug:
                print('\n Paths: ', paths)

        iters -= 1
        if iters == 0:
            return paths, result_paths

    return result_paths


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()
    array = np.array([list(line) for line in text])

    start = tuple(np.array(np.where(array == 'S')).flatten().tolist())
    end = tuple(np.array(np.where(array == 'E')).flatten().tolist())

    array = (array=='#').astype(int)
    pos = start
    direction = 0

    utils.show(array, start=start, end=end)

    paths = walk(array, start, end)

    paths = [(path, score(tuple(path))) for path in paths]
    pone = min(path[1] for path in paths)


    print(f"AOC {year} day {day}  Part One: {pone}")

    best_paths = [path for path in paths if path[1] == pone]

    tiles = set()
    for path in best_paths:
        tiles.update(set(path[0]))

    ptwo = len(tiles)
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
