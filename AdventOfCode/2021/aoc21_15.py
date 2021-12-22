# Advent of Code
year = 2021
day = 15

import numpy as np
import aocd
import itertools

text0 = """ 
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
"""

# text0 = """
# 113
# 152
# 181
# """

text1 = aocd.get_data(day=day, year=year)

moves = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]])
# moves = np.array([[0, -1], [-1, 0]])

pos_dict = dict()

def initial_result(arr):
    result = np.zeros(arr.shape, dtype=int)
    csr = np.cumsum(arr, axis=1)
    csc = np.cumsum(arr, axis=0)

    # First col and first row from cum sums
    result[0,:] = csr[0,:]
    result[:,0] = csr[:,0]


    for r in range(arr.shape[0]):
        pass


def make_paths(arr, result=None, iters=-1):
    if result is None or result.shape != arr.shape:
        result = np.full(arr.shape, fill_value=np.inf)
        result[0, 0] = 0

    stack = [tuple(x) for x in np.ndindex(arr.shape)]

    while len(stack) and iters != 0:
        iters -= 1
        coord = stack.pop(0)

        if coord == (0, 0):
            result[coord] = 0

        idx = moves + coord
        idx = [x for x in idx if (x >= (0, 0)).all() and (x < arr.shape).all()]
        loc = tuple(np.array(idx).T)
        score = result[loc].min() + arr[coord]
        if score < result[coord]:
            result[coord] = score
            for c in idx:
                if tuple(c) not in stack:
                    stack.append(tuple(c))

    return result.astype(int)


def validpath(p, arr):
    if p[0] != (0, 0):
        return False
    if p[-1] != arr.shape:
        return False

    for (a0, a1), (b0, b1) in zip(p[:-1], p[1:]):
        if abs(a1-a0) + abs(b1-b0) > 1:
            return False
    return True


def score_path(p, arr):
    idx = tuple(np.array(p).T)
    return arr[idx].sum()


def print_path(arr, path):
    if path is None:
        path = []
    result = ''
    for r in range(arr.shape[0]):
        for c in range(arr.shape[1]):
            if c == 0 and len(result):
                result += '\n'
            if (r, c) in path:
                result += '\033[36m' + str(arr[r,c]) + '\033[0m'
            else:
                result += str(arr[r,c])
    print(result)


def grad_descent(arr):
    path = [(arr.shape[0]-1, arr.shape[1]-1)]
    coord = path[0]
    for _ in range(np.product(arr.shape)):
        idx = moves + coord
        scores = [arr[tuple(x)] if (x >= (0, 0)).all() and (x < arr.shape).all() else np.inf for x in idx]
        coord = tuple(idx[np.argmin(scores)])
        path.append(coord)

        if coord == (0, 0):
            return path

    raise ValueError("No valid path found")


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text0
    text = text.strip().splitlines()

    arr = np.array([list(x) for x in text]).astype(int)
    # arr[0, 0] = 0
    # print(arr)

    result = make_paths(arr)
    # print(result)

    pone = result[-1, -1] - result[0, 0]
    print(f"AOC {year} day {day}  Part One: {pone}")

    arr2 = arr
    for c in range(1, 5):
        arr2 = np.append(arr2, arr + c, axis=1)
    row = arr2
    for r in range(1, 5):
        arr2 = np.append(arr2, row + r, axis=0)
    arr2 = (arr2 - 1) % 9 + 1
    arr2[(0, 0)] = 0

    result2 = np.append(result.astype(int), np.full(shape=(result.shape[0], result.shape[1]*4), fill_value=np.inf), axis=1)
    result2 = np.append(result2, np.full(shape=(result.shape[0]*4, result.shape[1]*5), fill_value=np.inf), axis=0)

    result2 = make_paths(arr2, result=result2)
    ptwo = result2[-1, -1] - result2[0, 0]

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
