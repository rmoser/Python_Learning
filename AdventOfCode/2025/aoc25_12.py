# Advent of Code

year = 2025
day = 12

import numpy as np
import aocd
import os
import utils
from pprint import pprint
from icecream import ic
import scipy as sp
import itertools as it

text0 = """0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2
"""
text1 = aocd.get_data(day=day, year=year)

boxes = []
tiles = []
tile_map = {}
tile_map_reverse = {}
tile_map_array = None
tile_interference = None
# n_tiles = (0, 0)

def init_tiles(boxes):
    global tiles, tile_map, tile_map_array #, n_tiles
    tiles = [np.zeros((3,3), dtype=int)]  # tile value 0 represents an empty space
    tile_map = {0: 0}
    for box, tile in boxes.items():
        tile_map[box] = set()
        for _ in range(4):
            for t in (tile, np.fliplr(tile)):
                if not arr_in_list(t, tiles):
                    tiles.append(t)
                    tile_map[box].add(len(tiles) - 1)
                    tile_map_reverse[len(tiles) - 1] = box
            tile = np.rot90(tile)

    # n_tiles = (1, len(tiles))
    tile_map_array = np.zeros((len(tiles), len(boxes)), dtype=int)
    for b in range(len(boxes)):
        for t in tile_map[b]:
            tile_map_array[t, b] = 1

    init_spatial_interferences()
    return tiles, tile_map, tile_map_array, tile_interference

def init_arr(size=None, tree=None, dtype=np.int8):
    if size is None and tree is None:
        raise ValueError('size or tree must be specified')
    elif tree is not None:
        size = sum(tree[1]), tree[0][0]-2, tree[0][1]-2
    return np.zeros(size, dtype=dtype)

def arr_in_list(arr, list):
    return any((a==arr).all() for a in list)

def box_count(arr):
    counts = np.bincount(arr[np.bitwise_and(0 <= arr, arr<len(tiles))], minlength=len(tiles))
    return tuple(counts.dot(tile_map_array).tolist())

def is_valid(arr):
    # All values between 0 and num(tiles), inclusive
    if not (0 <= arr.min() <= arr.max() < len(tiles)):
        return False

    # Only one tile per coordinate
    _arr = calculate_placements(arr)
    if not (_arr.sum(axis=0) <= 1).all():
        return False  # Tiles overlap

    return True


def is_solution(arr, tree):
    if not is_valid(arr):
        return False
    answer = np.array(tree[1])
    total = box_count(arr)
    if not len(total) == answer.shape[0]:
        return False
    return (total == answer).all()


def calculate_placements(arr):
    size = (np.array(arr.shape) + (0, 2, 2)).tolist()  # add space to expand placement flag to the full tile 3x3 area
    _arr = init_arr(size)

    for r, row_data in enumerate(arr):
        tile_num = row_data.max()
        if 0 < tile_num < len(tiles):
            try:
                _arr[r] = sp.signal.convolve(row_data>0, tiles[tile_num])
            except IndexError:
                ic(tile_num)
                raise
    return _arr

def init_spatial_interferences():
    global tile_interference
    tile_interference = np.full(shape=(len(tiles), 5, 5), dtype=object, fill_value=None)
    tile_interference[0] = set(range(len(tiles)))

    offsets = list(it.product(range(5), repeat=2))
    offsets.remove((2,2))  # Remove center of 5x5 grid, where tile is placed

    for tile0 in range(1, len(tiles)):
        tile_interference[(tile0, 2, 2)] = {tile0}
        for offset in offsets:
            tile_interference[(tile0, ) + offset] = {0}  # Init empty set
            for tile1 in range(1, len(tiles)):
                interference_arr = init_arr((2,5,5))
                interference_arr[0,2,2] = tile0
                interference_arr[(1,) + offset] = tile1
                if is_valid(interference_arr):
                    tile_interference[(tile0, ) + offset].add(tile1)



class TileMap:
    @staticmethod
    def compare(a, b):
        if isinstance(a, int):
            if isinstance(b, int):
                return a == b
            else:
                return a in b
        if isinstance(b, int):
            return b in a
        return bool(a & b)

    def __init__(self, tree):
        self.tree = tree
        self.size = tree[0][0]+2, tree[0][1]+2
        self.ans = tree[1]
        self.budget = list(self.ans)

        self.arr = np.fromfunction(np.vectorize(lambda i, j: set()), self.size) | set(range(len(tiles)))
        self.arr[:2] &= {0}
        self.arr[-2:] &= {0}
        self.arr[:,:2] &= {0}
        self.arr[:,-2:] &= {0}
        self.arr_placements = np.zeros_like(self.arr, dtype=int)
        self.refresh()


    def __repr__(self):
        s = f'{self.tree}\n\n'
        s += utils.show_string(self.tiles(), translate={48: '·'})
        # for row in np.arange(self.arr.shape[0]):
        #     s += ' '.join((f"{str(next(iter(t))) if len(t) == 1 else '..':>2}" for t in self.arr[row])) + '\n'
        return s

    def __getitem__(self, pos):
        if isinstance(pos, tuple) and len(pos) == 2:
            return self.arr[pos]
        raise IndexError(f'{pos} is not a valid index')

    def __setitem__(self, pos, value):
        if not isinstance(pos, tuple) and len(pos) == 2:
            raise IndexError(f'{pos} is not a valid index')
        if isinstance(value, set):
            self.arr[pos] = value
        elif value == 0:
            self.arr[pos] = set(range(len(tiles)))
        else:
            self.arr[pos] = value

    def window(self, pos):
        return self.arr[pos[0]-2:pos[0]+3, pos[1]-2:pos[1]+3].view()

    def add_tile(self, tile: int, pos: tuple[int, int]):
        if not tile in self.arr[pos]:
            raise ValueError(f"Tile {tile} does not fit at {pos}")

        # Insert tile at pos
        self.arr_placements[pos] = tile
        self.budget[tile_map_reverse[tile]] -= 1

        # a = self.window(pos)
        # b = tile_interference[tile][:a.shape[0], :a.shape[1]]
        # a &= b

        # self.refresh()
        self.update(pos)


    def remove_tile(self, pos: tuple[int, int]):
        tile = self.arr_placements[pos]
        self.arr_placements[pos] = 0
        self.budget[tile_map_reverse[tile]] += 1

        # Reset self.arr for affected range
        for r in range(max(2, pos[0]-2), min(pos[0]+3, self.arr.shape[0]-2)):
            for c in range(max(2, pos[1]-2), min(pos[1]+3, self.arr.shape[1]-2)):
                if self.arr_placements[r,c] == 0:
                    self.arr[r, c] = set(range(len(tiles)))
        # Reapply constraints
        for p in zip(*self.arr_placements.nonzero()):
            if pos[0]-4 <= p[0] <= pos[0]+2 and pos[1]-4 <= p[1] <= pos[1]+2:
                self.update(p)
        # for p in np.ndindex(self.window(pos).shape):
        #     self.arr[p] = set(range(len(tiles)))
        # self.update(pos)
        # self.refresh()


    # Scan the entire array and apply constraints
    def refresh(self):
        # Re-init arr
        for i in np.ndindex(self.arr.shape):
            if i[0] < 2 or i[1] < 2:
                self.arr[i] = {0}
                continue
            if i[0] > self.arr.shape[0]-3 or i[1] > self.arr.shape[1]-3:
                self.arr[i] = {0}
                continue
            self.arr[i] = set(range(len(tiles)))

        if not self.arr_placements.any():
            return

        for i in zip(*self.arr_placements.nonzero()):
            s = self.arr_placements[i]
            self.add_tile(s, i)
            # for j in np.ndindex(interference.shape):
            #     if j == (0, 0):
            #         continue
            #     p = i[0] + j[0], i[1] + j[1]
            #     if p[0] >= _arr.shape[0] or p[1] >= _arr.shape[1]:
            #         continue
            #     _arr[p] &= interference[j]

    def calculate_placements(self):
        _arr = np.zeros(self.tree[0], dtype=int)

        # for i in np.ndindex(self.arr_placements.shape):
        for i in zip(*self.arr_placements.nonzero()):
            t = self.arr_placements[i]
            tile = tiles[t]
            _arr[i[0]-2:i[0]+1, i[1]-2:i[1]+1] += tile
        return _arr

    # Update affected nearby positions
    def update(self, pos: tuple[int, int]):
        tile = self.arr_placements[pos]
        if tile == 0:
            return

        a = self.window(pos)
        b = tile_interference[tile] # [:a.shape[0], :a.shape[1]]
        a &= b

        return

        for other_pos in it.product(
                np.arange(max(0, pos[0]-2), min(self.size[0], pos[0]+3)),
                np.arange(max(0, pos[1]-2), min(self.size[1], pos[1]+3))
        ):
            ic(pos, other_pos)
            self._update(pos, other_pos)

    def _update(self, this: tuple[int, int], other: tuple[int, int]) -> bool:
        if this == other:
            return False

        this_tile = self.arr_placements[this] if self.arr_placements[this] else self.arr[this]
        other_tile = self.arr[other]

        if isinstance(this_tile, int) and isinstance(other_tile, int):
            return False

        if isinstance(this_tile, set) and isinstance(other_tile, set):
            return False

        if isinstance(this_tile, np.int64):

            # Check for this tile's impact on other tiles
            _arr = self.arr[this[0]:other[0] + 1, this[1]:other[1] + 1].view()
            if _arr.shape > (0,0):  # other tile is below or right of this tile
                offset = (_arr.shape[0]-1, _arr.shape[1]-1)
                # this tile impacts other tile IFF this tile is fixed
                other_tile &= tile_interference[this_tile][offset]
                return True

            _arr = self.arr[other[0]:this[0] + 1, other[1]:this[1] + 1].view()
            if _arr.shape > (0,0):  # other tile is below or right of this tile
                offset = (_arr.shape[0]-1, _arr.shape[1]-1)
                # this tile impacts other tile IFF this tile is fixed
                for x in list(other_tile):
                    if this_tile not in tile_interference[x][offset]:
                        other_tile.remove(x)
                return True

        else:  # other_tile is int
            # Check for other tile's impact on this tile
            _arr = self.arr[other[0]:this[0] + 1, other[1]:this[1] + 1].view()
            if _arr.shape > (0,0):  # other tile is above or left of this tile
                offset = (_arr.shape[0]-1, _arr.shape[1]-1)
                this_tile &= tile_interference[other_tile][offset]
                return True

        return False

    def box_count(self) -> np.ndarray:
        return np.bincount(self.boxes().flatten(), minlength=len(self.ans)+1)[:-1]

    def tiles(self, arr=None) -> np.ndarray:
        if arr is None:
            arr = self.arr_placements[2:-2,2:-2]
        return np.vectorize(lambda x: x if isinstance(x, int) else 0)(arr)

    def boxes(self) -> np.ndarray:
        return np.vectorize(lambda x: tile_map_reverse[x] if x>0 else len(self.ans))(self.tiles())

    def lens(self):
        return np.vectorize(lambda x: len(x))(self.arr)-1

    def len_order(self):
        return zip(*np.unravel_index(np.argsort(self.lens(), axis=None, stable=True), self.arr.shape))

    def is_valid(self) -> bool:
        # All values between 0 and num(tiles), inclusive
        # if not (0 <= self.arr.min() <= self.arr.max() < n_tiles[1]):
        #     return False

        # Only one tile per coordinate
        _arr = self.calculate_placements()
        if not (0 <= _arr.min() <= _arr.max() <= 1).all():
            return False  # Tiles overlap
        return True


    def is_solution(self) -> bool:
        if not self.is_valid():
            return False
        answer = self.ans
        total = self.box_count()
        if not len(total) == len(answer):
            return False
        return (total == answer).all()


    def solve_simple(self):
        total_box_area = sum(boxes[i].sum() * self.ans[i] for i in range(len(self.ans)))
        return total_box_area <= self.tree[0][0] * self.tree[0][1]

    def solve(self, recurse=True):
        total_box_area = sum(boxes[i].sum() * self.ans[i] for i in range(len(self.ans)))
        if total_box_area <= self.tree[0][0] * self.tree[0][1]:
            return tuple()  # No solution possible

        # if sum(self.ans) * 9 <= np.multiply(*self.tree[0]):
        #     return self.ans
        #
        if self.is_solution():
            return tuple(self.box_count().tolist())

        # Solve loop
        for pos in self.len_order():
            if self.arr_placements[pos] > 0 or len(self[pos]) <= 1:
                continue
            ic(f'solve has options at {pos}: {self.arr[pos]}')
            for t in list(self.arr[pos]):
                if t > 0:
                    b = tile_map_reverse[t]
                    if self.box_count()[b] >= self.ans[b]:
                        continue
                    if t not in self.arr[pos]:
                        continue

                    ic(f'solve adds tile {t} at {pos}: {self.arr[pos]}')
                    self.add_tile(t, pos)
                    ic(self.budget)
                    if self.is_solution():
                        return tuple(self.box_count().tolist())
                    if not recurse:
                        return
                    ans = self.solve()
                    if ans:
                        return ans
                    ic(f'solve rems tile {self.arr_placements[pos]} at {pos}...')
                    self.remove_tile(pos)
        ic('No solution...')
        return tuple()


def calculate_interferences(arr, interference_arr=None) -> np.ndarray:
    # _arr = calculate_placements(arr).sum(axis=0)
    _arr = arr.sum(axis=0)  # Collapse
    if interference_arr is None:
        interference_arr = np.empty_like(_arr)

    for i in zip(*_arr.nonzero()):
        tile = _arr[i]
        interference = tile_interference[tile]
        for offset in np.ndindex(interference_arr.shape):
            pos = i[0] + offset[0], i[1] + offset[1]
            if pos[0] < interference_arr.shape[0] and pos[1] < interference_arr.shape[1]:
                interference_arr[pos] &= interference[offset]

    return interference_arr



def display_placements(arr):
    for i in np.array(list(zip(*np.where(arr)))).tolist():
        print(i, ":", arr[tuple(i)])

def render(arr):
    return calculate_placements(arr).sum(axis=0)

def select_next_box(arr, tree):
    remaining = np.array(box_count(arr)) - tree[1]
    return (remaining > 0).argmax()


def solve_tree(tree):
    # Valid area for placements is 2 less, since each tile is 3x3
    size = tree[0][0]-2, tree[0][1]-2

    _box_count = sum(tree[1])  # Total number of boxes required for solution

    # Box placement array has one row for each box to place
    arr = init_arr((_box_count, ) + size)

    _solve_tree(arr, tree)

    if is_solution(arr, tree):
        return tuple(box_count(arr).tolist())
    return tuple()


def _solve_tree(arr, tree):
    # Simple flow:
    # 1. If no more tiles need to be placed, return True
    # 2. Find the next open row and next tile to place
    # 3. Loop through all valid placements, updating arr[row]
    # 4.    Recursive call to self on arr
    # 5. If we ran out of valid placements, return False
    # Return the value of the recursive call

    _box_count = sum(tree[1])  # Total number of boxes required for solution

    # Check for done
    if _box_count == 0:
        return True

    # Find next row to add a tile
    nonempty_rows = np.where(arr)[0]
    row = (nonempty_rows.argmax()+1) if nonempty_rows.size else 0

    # Check for out of rows
    if row >= arr.size[0]:
        return False

    # Map possible locations for placing a tile
    box = np.where(tree[1])[0].max()
    for t in tile_map[box]:
        for position in it.product(1, range(len(tiles))):
            pass

    for tile_num in range(1, len(tiles)):
        for t in tile_map[tile_num]:
            for iter_set in it.product(range(1, len(tiles))):
                pass



if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().split('\n\n')

    trees = text[-1].splitlines()
    for i, v in enumerate(trees):
        trees[i] = v.split(': ')
        trees[i][0] = tuple((int(x) for x in trees[i][0].split('x')))
        trees[i][1] = tuple((int(x) for x in trees[i][1].split()))


    boxes = dict()
    for box in text[:-1]:
        k = int(box.split(':')[0])
        v = (np.array([list(line) for line in box.splitlines()[1:]]) == '#').astype(int)
        boxes[k] = v
        # v = (np.array([list(line) for line in box.splitlines()[1:]]) == '#').astype(int)
        # boxes[k] = list(zip(*np.array(np.where(v)).tolist()))

    init_tiles(boxes)

    ic.disable()

    # pone = 0
    # for t, tree in enumerate(trees):
    #     tm = TileMap(tree)
    #     print(f'Tree {t}: {tree}...')
    #     tm.solve_simple()
    #     if tm.is_solution():
    #         print(f'Tree {t}: solved: {tm.ans}')
    #         pone += 1
    #     else:
    #         print(f'Tree {t}: no solution.')

    pone = sum(bool(TileMap(tree).solve_simple()) for tree in trees)

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
