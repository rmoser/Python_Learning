# Advent of Code
year = 2021
day = 18

import numpy as np
import aocd
import math
import itertools


def add(a, b):
    return f'[{a},{b}]'

text0 = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
"""

text1 = aocd.get_data(day=day, year=year)

digits = set('0123456789')


def reduce(a):
    iter = 0
    # print(f"iter {iter}:         {a}")
    while True:
        iter += 1
        # Explode
        depths = depth(a)
        i = np.argmax(depths > 4)  # left bracket of the 4-nested pair
        if depths[i] > 4:
            a = explode_pair(a, i)
            # print(f"iter {iter}: explode {a}")
            continue

        # Split
        vals = np.array(get_vals(a), dtype=int)
        i = np.argmax(vals > 9)
        if vals[i] > 9:
            l = a.find(str(vals[i]))
            a = split_num(a, l)
            # print(f"iter {iter}: split   {a}")
            continue

        break

    return a


def depth(a):
    arr = [int(c in '[]') * (1 if c == '[' else -1) for c in a]
    return np.cumsum(arr)


def explode_pair(a, l):
    # l should denote the index of the left bracket
    if not a[l] == '[':
        raise IndexError(f"Index {l} not [: {a} = {a[l]}")
    r = l + a[l:].find(']') + 1
    l = a[:r].rfind('[')

    left, pair, right = a[:l], a[l:r], a[r:]
    other_lval = right_val(left)
    other_rval = left_val(right)
    my_lval, my_rval = get_vals(pair)

    if len(other_lval) == 0:
        new_lval = ''
    else:
        new_lval = str(int(other_lval) + int(my_lval))
    idx_l = left.rfind(other_lval)
    new_left_string = left[:idx_l] + new_lval + left[idx_l+len(other_lval):]

    if len(other_rval) == 0:
        new_rval = ''
    else:
        new_rval = str(int(other_rval) + int(my_rval))
    idx_r = right.find(other_rval)
    new_right_string = right[:idx_r] + new_rval + right[idx_r+len(other_rval):]

    return new_left_string + '0' + new_right_string


def split_num(a, l):
    if a[l] not in digits:
        raise IndexError(f"Index {l} not numeric: {a} = {a[l]}")
    r = l + next(i for i,c in enumerate(a[l:]) if c not in digits)

    left, num, right = a[:l], a[l:r], a[r:]
    n = int(num) / 2
    l = math.floor(n)
    r = math.ceil(n)

    return f'{left}[{l},{r}]{right}'


def get_vals(a):
    return a.translate(a.maketrans('[],', '   ')).strip().split()


def get_delims(a):
    return a.translate(a.maketrans('0123456789', '          ')).strip().split()


def right_val(a):
    s = get_vals(a)
    if len(s):
        return s[-1]
    return ''


def left_val(a):
    s = get_vals(a)
    if len(s):
        return s[0]
    return ''


def magnitude(a):
    iter = 0
    # print(f"iter {iter}: mag {a}")
    while True:
        iter += 1
        # Explode
        depths = depth(a)
        l = np.argmax(depths)  # left bracket of the deepest-nested pair

        if a[l] == '[':
            r = l + a[l:].find(']') + 1

            left, pair, right = a[:l], a[l:r], a[r:]
            # print(left, pair, right)
            a, b = [int(c) for c in get_vals(pair)]

            new = str(3 * a + 2 * b)

            a = left + new + right
            # print(f"iter {iter}: mag {a}")

        if '[' not in a:
            return int(a)


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    a = text[0]
    for b in text[1:]:
        a = reduce(add(a, b))

    pone = magnitude(a)
    print(f"AOC {year} day {day}  Part One: {pone}")


    results = []
    for a, b in itertools.permutations(range(len(text)), 2):
        results.append(magnitude(reduce(add(text[a], text[b]))))

    ptwo = max(results)
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
