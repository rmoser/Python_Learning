# Advent of Code
year = 2015
day = 21

import numpy as np
import aocd
import itertools
import math

text0 = """ 
Weapons:    Cost  Damage  Armor
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0

Armor:      Cost  Damage  Armor
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5

Rings:      Cost  Damage  Armor
Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3
"""
text1 = aocd.get_data(day=day, year=year)

COST = 0
HP = 0
DAM = 1
AC = 2


def play(p, b):
    patt = max(p[DAM] - b[AC], 1)
    batt = max(b[DAM] - p[AC], 1)

    p_rnd, p_hp = divmod(p[HP], batt)
    p_rnd += int(p_hp > 0)

    b_rnd, b_hp = divmod(b[HP], patt)
    b_rnd += int(b_hp > 0)

    if p_rnd >= b_rnd:
        return 1, (p_rnd, p_hp), (b_rnd, b_hp)

    return 0, (p_rnd, p_hp), (b_rnd, b_hp)


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text0
    text = text.strip().splitlines()

    weapons = {}
    armor = {'None': (0, 0, 0)}
    rings = armor.copy()
    d = {}  # Init
    for line in text:
        if ":" in line:
            if line[0] == 'W':
                d = weapons
            elif line[0] == 'A':
                d = armor
            else:
                d = rings
            continue
        if line:
            name = line[:12].strip()
            d[name] = tuple(int(x) for x in line[12:].split())

    # print(weapons)
    # print(armor)
    # print(rings)

    text = text1
    text = text.strip().splitlines()
    boss = []
    for line in text:
        boss.append(int(line.split()[-1]))

    player = [100, 0, 0]
    print("P: ", player)
    print("B: ", boss)

    games = []
    for w, a, l, r in itertools.product(weapons, armor, rings, rings):
        if l == r and l != 'None':
            continue

        cost = weapons[w][COST] + armor[a][COST] + rings[r][COST] + rings[l][COST]
        player[DAM] = weapons[w][DAM] + armor[a][DAM] + rings[r][DAM] + rings[l][DAM]
        player[AC] = weapons[w][AC] + armor[a][AC] + rings[r][AC] + rings[l][AC]
        # print("Game player: ", player)
        result = play(player, boss)
        games.append([result[0], cost, (w, a, l, r)])

    games_arr = np.array([g[:2] for g in games])

    arr_one = (9999 * (games_arr[:, 0] == 0) + (games_arr[:, 0] == 1)) * games_arr[:, 1]
    pone = arr_one.min()
    parg = np.argmin(arr_one)
    print(games[parg])

    # print(games_arr)
    print(f"AOC {year} day {day}  Part One: {pone}")

    arr_two =  (games_arr[:, 1] * (games_arr[:, 0] == 0))
    ptwo = arr_two.max()
    parg = np.argmax(arr_two)
    print(games[parg])

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
