# Advent of Code
year = 2021
day = 20

import numpy as np
import aocd
import itertools

text0 = """
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##
#..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###
.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#.
.#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#.....
.#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#..
...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.....
..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
"""

text2 = """
##...###...##.#..###.#...#....#..###.##.###...###.##.##.####.#######..######....#.###.##....#.##...#..........#####..##..#..##...##....####.###..#..####.##.##.#....#.##.#.#.#.#..##.##.#...##..##...#.#...#...#..#.#...#.##...#..######.#.##..#.#.#...##.###..########...........#.#.###.#.#..##...#..#..###..#..##.#.#...##..##..###..#####...#.####....#.###....###.##.##...##.#..#.#..####....#..##...##.#####.###.###.###.....##...#.#..#.######.##.##.......###...#.....#...##..#..#.###.#..#..########.##......###..##.#.

###·###
#···##·
·#·#··#
##·###·
#······
·###···
#######
"""

text1 = aocd.get_data(day=day, year=year)

grid = np.array([tuple(x) for x in itertools.product([-1,0,1], [-1,0,1])])


def show(image):
    s = '\n'.join([''.join(image[x].astype(str)) for x in range(image.shape[0])])
    print(s.translate(s.maketrans('01', chr(183)+'#')))


def enhance(image, algo, field=0):
    sh = np.array(image.shape) + 4
    # print(sh)

    in_image = np.full(shape=sh, fill_value=field)
    in_image[2:-2, 2:-2] = image.copy()
    # show(image)

    next_field = algo[9] if field else algo[0]

    i8 = in_image[:-2, :-2]
    i7 = in_image[:-2, 1:-1]
    i6 = in_image[:-2, 2:]
    i5 = in_image[1:-1, :-2]
    i4 = in_image[1:-1, 1:-1]
    i3 = in_image[1:-1, 2:]
    i2 = in_image[2:, :-2]
    i1 = in_image[2:, 1:-1]
    i0 = in_image[2:, 2:]

    idx = i8 * 256 + i7 * 128 + i6 * 64 + i5 * 32 + i4 * 16 + i3 * 8 + i2 * 4 + i1 * 2 + i0

    out_image = np.vectorize(lambda x: algo[x])(idx)

    # show(in_image)
    # print()
    # show(out_image)
    return out_image, next_field


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1

    algo, image = text.strip().split('\n\n')
    algo = algo.replace('\n', '')
    algo = (np.array(list(algo)) == '#').astype(int)

    image = image.splitlines()
    image = (np.array([list(x) for x in image]) == '#').astype(int)

    field = 0

    images = [image]
    fields = [field]

    for _ in range(2):
        image, field = enhance(image, algo, field)

    pone = image.sum()

    for _ in range(48):
        image, field = enhance(image, algo, field)

    ptwo = image.sum()

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
