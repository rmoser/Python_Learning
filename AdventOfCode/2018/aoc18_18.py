# Advent of Code
year = 2018
day = 18

import numpy as np
import aocd
import itertools
import utils

text0 = """
.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.
"""
text1 = aocd.get_data(day=day, year=year)

Adj = np.array([(0, 1), (0, -1), (1, 0), (1, -1), (1, 1), (-1, -1), (-1, 0), (-1, 1)])

Memo = dict()


def score(arr):
    _, s, _ = arr.shape
    if s % 10:
        return arr[1, 1:-1, 1:-1].sum() * arr[2, 1:-1, 1:-1].sum()
    else:
        return arr[1].sum() * arr[2].sum()


def run(arr, n=1, p=100000):
    _arr = np.zeros(shape=np.array(arr.shape) + (0, 2, 2), dtype=arr.dtype)
    _arr[:, 1:-1, 1:-1] = arr

    for i in range(n):
        k = tuple(_arr[1:, 1:-1, 1:-1].flatten())
        if k in Memo:
            _arr = Memo[k]
            if p > 0 and ((i + 1) % p) == 0:
                print(f'\r{i}: {score(_arr)}')
            # print('memo!')
            continue

        _new_fields = np.bitwise_and(
            _arr[2, 1:-1, 1:-1],  # Lumberyard converts to Field rule
            np.bitwise_not(
                np.bitwise_and(  # Lumberyards with at least 1 tree and at least one lumberyard remain lumberyards
                    np.any((
                        _arr[1, :-2, :-2], _arr[1, :-2, 1:-1], _arr[1, :-2, 2:],
                        _arr[1, 1:-1, :-2], _arr[1, 1:-1, 2:],
                        _arr[1, 2:, :-2], _arr[1, 2:, 1:-1], _arr[1, 2:, 2:]
                    ), axis=0),
                    np.any((
                        _arr[2, :-2, :-2], _arr[2, :-2, 1:-1], _arr[2, :-2, 2:],
                        _arr[2, 1:-1, :-2], _arr[2, 1:-1, 2:],
                        _arr[2, 2:, :-2], _arr[2, 2:, 1:-1], _arr[2, 2:, 2:]
                    ), axis=0)
                )
            )
        )

        _new_trees = np.bitwise_and(
            _arr[0, 1:-1, 1:-1],  # Field converts to Forest rule
            np.sum((
                _arr[1, :-2, :-2], _arr[1, :-2, 1:-1], _arr[1, :-2, 2:],
                _arr[1, 1:-1, :-2], _arr[1, 1:-1, 2:],
                _arr[1, 2:, :-2], _arr[1, 2:, 1:-1],  _arr[1, 2:, 2:]
            ), axis=0) >= 3
        )

        _new_lumberyards = np.bitwise_and(
            _arr[1, 1:-1, 1:-1],  # Forest converts to Lumberyard rule
            (np.sum((
                 _arr[2, :-2, :-2], _arr[2, :-2, 1:-1], _arr[2, :-2, 2:],
                 _arr[2, 1:-1, :-2], _arr[2, 1:-1, 2:],
                 _arr[2, 2:, :-2], _arr[2, 2:, 1:-1], _arr[2, 2:, 2:]
            ), axis=0) >= 3)
        )


        # _new = _arr.copy()
        # _arr[0, 1:-1, 1:-1] = np.bitwise_or(_new_fields, np.bitwise_and(_arr[0, 1:-1, 1:-1], np.bitwise_not(_new_trees)))
        # _arr[1, 1:-1, 1:-1] = np.bitwise_or(_new_trees, np.bitwise_and(_arr[1, 1:-1, 1:-1], np.bitwise_not(_new_lumberyards)))
        # _arr[2, 1:-1, 1:-1] = np.bitwise_or(_new_lumberyards, np.bitwise_and(_arr[2, 1:-1, 1:-1], np.bitwise_not(_new_fields)))

        _arr[:, 1:-1, 1:-1] = [
            np.bitwise_or(_new_fields, np.bitwise_and(_arr[0, 1:-1, 1:-1], np.bitwise_not(_new_trees))),
            np.bitwise_or(_new_trees, np.bitwise_and(_arr[1, 1:-1, 1:-1], np.bitwise_not(_new_lumberyards))),
            np.bitwise_or(_new_lumberyards, np.bitwise_and(_arr[2, 1:-1, 1:-1], np.bitwise_not(_new_fields)))
        ]

        if not (_arr[:, 1:-1, 1:-1].sum(axis=0) == 1).all():
            raise SyntaxError("Bad calculation.")

        Memo[k] = _arr

        if p > 0 and ((i+1) % p) == 0:
            print(f'\r{i}: {_arr[1].sum() * _arr[2].sum()}')
        # _arr = _arr.copy()
        # for y in range(_arr.shape[0]):
        #     for x in range(_arr.shape[1]):
        #         _new[y, x] = check(_arr, (y, x))
        # _arr[1:-1, 1:-1] = _new[1:-1, 1:-1]

    # print()
    return _arr[:, 1:-1, 1:-1]


def check(arr, c):
    y, x = c
    subarr = arr[:, max(0, y - 1):min(arr.shape[0], y + 2), max(0, x - 1):min(arr.shape[1], x + 2)].copy()
    subarr[min(y, 1), min(x, 1)] = False
    # show(subarr)
    if arr[0, y, x]:
        if subarr[1].sum() >= 3:
            return 1
    elif arr[1, y, x]:
        if subarr[2].sum() >= 3:
            return 2
    elif arr[2, y, x]:
        if not (subarr[1].any() & subarr[2].any()):
            return 0
    return sum(arr[:, y, x] * [0, 1, 2])


def show(my_arr):
    if isinstance(my_arr, tuple):
        my_arr = keymap(my_arr)

    if len(my_arr.shape) == 3:
        _arr = my_arr[1] + my_arr[2] * 2
        utils.show(_arr.astype(str), translate={ord('0'): ord('.'), ord('1'): ord('|'), ord('2'): ord('#')})
    else:
        utils.show(my_arr.astype(int).astype(str), translate={ord('0'): ord(' '), ord('1'): ord('X')})


def keymap(key):
    s = int(np.sqrt(len(key) / 2))
    a = np.zeros(shape=(3, s, s), dtype=bool)
    a[1] = np.array(key[:s*s]).reshape((s, s))
    a[2] = np.array(key[s*s:]).reshape((s, s))
    a[0] = np.bitwise_not(np.bitwise_or(a[1], a[2]))
    return a


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    Memo.clear()

    text = text1
    text = text.strip()
    if '\n' in text:
        text = text.strip('\n').splitlines()

    tarr = np.array([list(x) for x in text])
    tarr = (tarr == '|') + (tarr == '#')*2

    arr = np.zeros(shape=(3, ) + tarr.shape , dtype=bool)
    arr[0] = tarr == 0
    arr[1] = tarr == 1
    arr[2] = tarr == 2

    k = tuple(arr[1:].flatten())
    k_list = []
    _a = arr.copy()

    while k not in Memo:
        k_list.append(k)
        _a = run(_a, 1)
        k = tuple(_a[1:].flatten())

    pone = score(keymap(k_list[10]))
    print(f"AOC {year} day {day}  Part One: {pone}")

    loop_last_key = k_list[-1]
    loop_first_arr = Memo[loop_last_key]
    loop_first_key = tuple(loop_first_arr[1:, 1:-1, 1:-1].flatten())
    loop_first_index = k_list.index(loop_first_key)
    loop_last_index = len(k_list)
    loop_period = loop_last_index - loop_first_index
    loop_offset = len(k_list) - loop_period

    i = ((1000000000 - loop_offset) % loop_period) + loop_offset
    key_1_billion = k_list[i]
    ptwo = score(keymap(key_1_billion))
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
