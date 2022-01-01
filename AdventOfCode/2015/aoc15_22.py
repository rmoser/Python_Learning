# Advent of Code
year = 2015
day = 22

import numpy as np
import aocd
import enum

text0 = """ 
"""
text1 = aocd.get_data(day=day, year=year)

# Game state enums
P_HP = 0
B_HP = 1
MANA = 2
SHIELD = 3  # Match spell effect enum
RECHARGE = 4  # Match spell effect enum
POISON = 5  # Match spell effect enum
B_DAM = 6
AC = 7
WINNER = 8
PLAYER_WON = 8
TOTAL_COST = 9
SPELLS = 10

# Spell effect enums
COST = 0
DAM = 1
HEAL = 2
# SHIELD = 3
# RECHARGE = 4
# POISON = 5

spells = {
    #                COST  D  H  S  R  P
    'Magic Missile': ( 53, 4, 0, 0, 0, 0),
    'Drain':         ( 73, 2, 2, 0, 0, 0),
    'Shield':        (113, 0, 0, 6, 0, 0),
    'Poison':        (173, 0, 0, 0, 0, 6),
    'Recharge':      (229, 0, 0, 0, 5, 0)
}

min_mana = min(s[COST] for s in spells.values())


def new_game(player_hp, boss_hp, mana, boss_damage):
    return [player_hp, boss_hp, mana, 0, 0, 0, boss_damage, 0, -1, 0, []]


def status_effects(game):
    # Status effects before player move
    if game[RECHARGE]:
        game[RECHARGE] -= 1
        game[MANA] += 101
    if game[POISON]:
        game[POISON] -= 1
        game[B_HP] -= 3
    if game[SHIELD]:
        game[SHIELD] -= 1
    else:
        game[AC] = 0
    return game


def game_done(game):
    if game[P_HP] <= 0:
        game[WINNER] = 0
        return True
    if game[B_HP] <= 0:
        game[WINNER] = 1
        return True
    return False


def game_copy(game):
    g = game.copy()
    g[SPELLS] = g[SPELLS].copy()
    return g


def play(games, done=None, part=1):
    min_cost = np.inf

    if not isinstance(games[0], list):
        games = [games]
    if done is None:
        done = []

    for _ in range(len(games)):
        game = games.pop(0)

        if part == 2:
            game[P_HP] -= 1
            if game_done(game):
                done.append(game)
                continue

        game = status_effects(game)

        if game[MANA] < min_mana:  # Abort this branch
            continue

        for spell, effect in spells.items():
            # Skip invalid spells
            if game[MANA] < effect[COST]:  # Insufficient mana
                continue
            if any(game[s] and effect[s] for s in (SHIELD, POISON, RECHARGE)):  # Still in effect
                continue

            g = game_copy(game)
            g[SPELLS].append(spell)
            g[MANA] -= effect[COST]
            g[TOTAL_COST] += effect[COST]

            if g[TOTAL_COST] > min_cost:  # Abandon this branch
                continue

            if effect[DAM]:
                g[B_HP] -= effect[DAM]
            if effect[HEAL]:
                g[P_HP] += effect[HEAL]
            # These effects are mutually exclusive:
            if effect[SHIELD]:
                g[SHIELD] = effect[SHIELD]
                g[AC] = 7
            elif effect[POISON]:
                g[POISON] = effect[POISON]
            elif effect[RECHARGE]:
                g[RECHARGE] = effect[RECHARGE]

            # Boss' turn
            g = status_effects(g)

            if game_done(g):
                done.append(g)
                if g[PLAYER_WON]:
                    min_cost = min(min_cost, g[TOTAL_COST])
                continue

            # Boss attacks
            g[P_HP] -= max(1, g[B_DAM] - g[AC])

            if game_done(g):
                done.append(g)
                if g[PLAYER_WON]:
                    min_cost = min(min_cost, g[TOTAL_COST])
                continue

            # Keep playing
            games.append(g)

    return games, done


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    boss = []
    for line in text:
        boss.append(int(line.split()[-1]))

    print(boss)

    start = new_game(50, boss[0], 500, boss[1])

    # pone = 1824
    if not pone:
        games = [start]
        done = []
        i = 0
        while len(games):
            i += 1
            games, done = play(games, done)
        pone = min(g[TOTAL_COST] for g in done if g[PLAYER_WON])
        print(f"AOC {year} day {day}  Part One: {pone}")


    games = [start]
    done = []
    i = 0
    while len(games):
        i += 1
        games, done = play(games, done, part=2)
        print(i, "games: ", len(games), "done: ", len(done))
    ptwo = min(g[TOTAL_COST] for g in done if g[PLAYER_WON])
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
