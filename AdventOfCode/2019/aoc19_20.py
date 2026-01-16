# Advent of Code
year = 2019
day = 20

import numpy as np
import aocd
from pprint import pprint
import utils
import itertools as it
from icecream import ic


text0 = """
         A           
         A           
  #######.#########  
  #######.........#  
  #######.#######.#  
  #######.#######.#  
  #######.#######.#  
  #####  B    ###.#  
BC...##  C    ###.#  
  ##.##       ###.#  
  ##...DE  F  ###.#  
  #####    G  ###.#  
  #########.#####.#  
DE..#######...###.#  
  #.#########.###.#  
FG..#########.....#  
  ###########.#####  
             Z       
             Z       
"""

text2 = """
                   A               
                   A               
  #################.#############  
  #.#...#...................#.#.#  
  #.#.#.###.###.###.#########.#.#  
  #.#.#.......#...#.....#.#.#...#  
  #.#########.###.#####.#.#.###.#  
  #.............#.#.....#.......#  
  ###.###########.###.#####.#.#.#  
  #.....#        A   C    #.#.#.#  
  #######        S   P    #####.#  
  #.#...#                 #......VT
  #.#.#.#                 #.#####  
  #...#.#               YN....#.#  
  #.###.#                 #####.#  
DI....#.#                 #.....#  
  #####.#                 #.###.#  
ZZ......#               QG....#..AS
  ###.###                 #######  
JO..#.#.#                 #.....#  
  #.#.#.#                 ###.#.#  
  #...#..DI             BU....#..LF
  #####.#                 #.#####  
YN......#               VT..#....QG
  #.###.#                 #.###.#  
  #.#...#                 #.....#  
  ###.###    J L     J    #.#.###  
  #.....#    O F     P    #.#...#  
  #.###.#####.#.#####.#####.###.#  
  #...#.#.#...#.....#.....#.#...#  
  #.#####.###.###.#.#.#########.#  
  #...#.#.....#...#.#.#.#.....#.#  
  #.###.#####.###.###.#.#.#######  
  #.#.........#...#.............#  
  #########.###.###.#############  
           B   J   C               
           U   P   P               
"""
text3 = """             Z L X W       C                 
             Z P Q B       K                 
  ###########.#.#.#.#######.###############  
  #...#.......#.#.......#.#.......#.#.#...#  
  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  
  #.#...#.#.#...#.#.#...#...#...#.#.......#  
  #.###.#######.###.###.#.###.###.#.#######  
  #...#.......#.#...#...#.............#...#  
  #.#########.#######.#.#######.#######.###  
  #...#.#    F       R I       Z    #.#.#.#  
  #.###.#    D       E C       H    #.#.#.#  
  #.#...#                           #...#.#  
  #.###.#                           #.###.#  
  #.#....OA                       WB..#.#..ZH
  #.###.#                           #.#.#.#  
CJ......#                           #.....#  
  #######                           #######  
  #.#....CK                         #......IC
  #.###.#                           #.###.#  
  #.....#                           #...#.#  
  ###.###                           #.#.#.#  
XF....#.#                         RF..#.#.#  
  #####.#                           #######  
  #......CJ                       NM..#...#  
  ###.#.#                           #.###.#  
RE....#.#                           #......RF
  ###.###        X   X       L      #.#.#.#  
  #.....#        F   Q       P      #.#.#.#  
  ###.###########.###.#######.#########.###  
  #.....#...#.....#.......#...#.....#.#...#  
  #####.#.###.#######.#######.###.###.#.#.#  
  #.......#.......#.#.#.#.#...#...#...#.#.#  
  #####.###.#####.#.#.#.#.###.###.#.###.###  
  #.......#.....#.#...#...............#...#  
  #############.#.#.###.###################  
               A O F   N                     
               A A D   M                     """

text1 = aocd.get_data(day=day, year=year)


def valid_path_netr(maze, start, end, recursive=0, paths=None, iters=-1, debug=False):
    if not paths:
        paths = [[start]]
    elif not isinstance(paths[0], list):
        paths = [paths]

    pos_dist = {start: 0}

    # max_moves = np.prod(maze.shape)

    result_paths = []

    while True:
        for _ in range(len(paths)):
            path = paths.pop(0)
            # if len(path) >= max_moves:
            #     return []

            pos = path[-1]
            for new_pos in list(maze[pos[:2] + (0, )]):
                if recursive:  # Tuple element 2 is additive (depth)
                    new_pos = new_pos[:2] + (pos[2] + new_pos[2], )
                    if new_pos[2] < 0:
                        continue
                # new_pos = pos + move  # type is np.array
                # new_pos_tuple = tuple(new_pos)
                # if (new_pos < 0).any() or (new_pos >= maze.shape).any():
                #     continue
                if new_pos == end:
                    pos_dist[new_pos] = len(path)  # len(path) includes the start point already, so no need to increment for the end point
                    return path + [new_pos], pos_dist
                if new_pos in pos_dist:  # Shorter path to this point already exists
                    continue
                paths.append(path + [new_pos])
                pos_dist[new_pos] = len(path)  # len(path) includes the start point already, so no need to increment for the end point

                ic(pos, new_pos, len(path))

            # ic('\n Paths: ', paths)

        iters -= 1
        if iters == 0:
            return paths, pos_dist


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    if '\n' in text:
        text = text.splitlines()

    maze = np.array([list(line) for line in text if line])
    nodes = dict()
    portals = dict()

    # Add all nodes
    for r, c in np.ndindex(maze.shape):
        if maze[r, c] != '.':
            continue
        nodes[(r, c, 0)] = set()
        for _r, _c in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            p0 = r + _r, c + _c
            if maze[p0] == '.':
                nodes[(r, c, 0)].add(p0 + (0, ))
            elif maze[p0] == '#':
                continue
            else:
                p1 = r + 2 * _r, c + 2 * _c
                if p0 < p1:
                    portal_name = maze[p0] + maze[p1]
                else:
                    portal_name = maze[p1] + maze[p0]
                if not portal_name in portals:
                    portals[portal_name] = set()
                portals[portal_name].add((r, c))

    # Add all portals
    for portal in portals.values():
        if len(portal) == 2:
            a, b = portal
            if 2 in a or a[0] == maze.shape[0]-3 or a[1] == maze.shape[1]-3:
                nodes[a + (0, )].add(b + (-1, ))
                nodes[b + (0, )].add(a + (1, ))
            else:
                nodes[a + (0, )].add(b + (1, ))
                nodes[b + (0, )].add(a + (-1, ))

            # if 2 in b or b[0] == maze.shape[0]-2 or b[1] == maze.shape[1]-2:
            #     nodes[b + (0, )].add(a + (-1, ))
            # else:
            #     nodes[b + (0, )].add(a + (1, ))

    start = iter(portals['AA']).__next__() + (0, )
    end = iter(portals['ZZ']).__next__() + (0, )

    ans = valid_path_netr(nodes, start, end)
    pone = ans[1][end]

    ans = valid_path_netr(nodes, start, end, recursive=1)
    ptwo = ans[1][end]

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
