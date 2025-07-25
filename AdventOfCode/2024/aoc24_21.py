# Advent of Code
import itertools

year = 2024
day = 21

import numpy as np
import aocd
import os
import functools
from pprint import pprint
# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

text0 = """
029A
980A
179A
456A
379A
"""
text1 = aocd.get_data(day=day, year=year)

NUMBER_BUTTONS = {
        '7': (3, 2), '8': (3, 1), '9': (3, 0),
        '4': (2, 2), '5': (2, 1), '6': (2, 0),
        '1': (1, 2), '2': (1, 1), '3': (1, 0),
        # 'X': (0, 2),
        '0': (0, 1), 'A': (0, 0)
    }
for k, v in list(NUMBER_BUTTONS.items()):
    NUMBER_BUTTONS[k] = np.array(v, dtype=int)
    NUMBER_BUTTONS[v] = k

DIRECTIONAL_BUTTONS = {(0, 0): 'A', (0, 1): '^', (-1, 2): '<', (-1, 1): 'v', (-1, 0): '>'}
for k, v in list(DIRECTIONAL_BUTTONS.items()):
    DIRECTIONAL_BUTTONS[v] = np.array(k, dtype=int)

DIRECTIONS = {'v': (-1, 0), '^': (1, 0), '<': (0, 1), '>': (0, -1)}
for k, v in list(DIRECTIONS.items()):
    DIRECTIONS[k] = np.array(v, dtype=int)

def check(pos: tuple, code: str, as_numeric=False):
    _pos = pos
    for c in code:
        if c == 'A':
            continue
        _pos = tuple((_pos + DIRECTIONS[c]).tolist())
        if as_numeric and _pos not in NUMBER_BUTTONS:
            return False
        if not as_numeric and _pos not in DIRECTIONAL_BUTTONS:
            return False
    return True


def numeric(code, n=2) -> dict:
    buttons = NUMBER_BUTTONS
    dirs = DIRECTIONS

    result = dict()
    pos = tuple(buttons['A'].tolist())
    # print(code)
    for c in code:
        new_pos = buttons[c]
        move = new_pos - pos
        new_pos = tuple(new_pos.tolist())
        word = ''
        # print(c, pos, new_pos, move)
        if move[0] > 0:
            word += '^' * move[0]
        if move[1] < 0:
            word += '>' * -move[1]
        if move[0] < 0:
            word += 'v' * -move[0]
        if move[1] > 0:
            word += '<' * move[1]

        if bool(word) and word[0] != word[-1] and check(pos, word[::-1] + 'A', as_numeric=True):
            word_options = np.unique([word, word[::-1]])
            encoded_lengths = [get_len(directional(x+'A', n-1)) for x in word_options]
            print(word_options)
            print(encoded_lengths)
            word = word_options[encoded_lengths.index(min(encoded_lengths))]
            # print(word_options, encoded_lengths, word)

        word += 'A'
        result[word] = result.get(word, 0) + 1
        pos = new_pos


    return result

    # # Decode because forward == False
    # for c in code:
    #     if c == 'A':
    #         result += buttons[pos]
    #         continue
    #
    #     new_pos = tuple((np.array(pos) + dirs[c]).tolist())
    #     if buttons[new_pos] == 'X':
    #         raise f"Halt for leaving the button area: {code}"
    #     pos = new_pos
    # return result

def get_len(code):
    return sum(len(k) * v for k, v in code.items())

@functools.cache
def _directional(code: str, n:int) -> dict:
    if n == 0:
        return {code: 1}

    buttons = DIRECTIONAL_BUTTONS

    dirs = DIRECTIONS

    result = dict()
    pos = tuple(buttons['A'].tolist())
    # print(code)
    for c in code:
        new_pos = buttons[c]
        move = new_pos - pos
        new_pos = tuple(new_pos.tolist())
        word = ''
        # print(c, pos, new_pos, move)
        if move[0] < 0:
            word += 'v' * -move[0]
        if move[1] < 0:
            word += '>' * -move[1]
        if move[0] > 0:
            word += '^' * move[0]
        if move[1] > 0:
            word += '<' * move[1]

        if bool(word) and word[0] != word[-1] and check(pos, word[::-1] + 'A'):
            word_options = np.unique([word, word[::-1]])
            # print(word_options)
            encoded_lengths = [get_len(directional(x+'A', n-1)) for x in word_options]
            word = word_options[encoded_lengths.index(min(encoded_lengths))]
            # print(word_options, encoded_lengths, word)

        word += 'A'
        result[word] = result.get(word, 0) + 1
        pos = new_pos
    return result

def directional(code, n=1) -> dict:
    if not isinstance(code, dict):
        _code = [c + 'A' for c in code.split('A')[:-1]]
        code = dict()
        for c in _code:
            code[c] = code.get(c, 0) + 1

    result = code  # Default result if n == 0

    for i in range(n, 0, -1):
        result = dict()
        for k, v in code.items():
            for _k, _v in _directional(k, i).items():
                result[_k] = result.get(_k, 0) + _v * v
        code = result
    return result


def encode(code):
    if set(code) & set('<>^v'):
        return directional(code)
    else:
        return numeric(code)

# def decode(code, as_numeric=False):
#     if as_numeric:
#         return numeric(code, forward=False)
#     return directional(code, forward=False)


if __name__ == '__main__':
    pone = np.int64(0)
    ptwo = np.int64(0)

    text = text1
    text = text.strip().splitlines()

    for code in text:
        val = int(code[:-1])
        code = numeric(code, 3)
        code = directional(code, 2)
        pone += get_len(code) * val

    for code in text:
        val = int(code[:-1])
        code = numeric(code, 26)
        code = directional(code, 25)
        ptwo += get_len(code) * val

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
