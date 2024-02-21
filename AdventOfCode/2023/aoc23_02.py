# Advent of Code
year = 2023
day = 2

import numpy as np
import aocd

text0 = """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""
text1 = aocd.get_data(day=day, year=year)

new_bag = {'red': 0, 'blue': 0, 'green': 0}


def parse(s):
    bag = new_bag.copy()
    for b in s.split("; "):
        for c in b.split(", "):
            # print(c)
            n, color = c.split()
            # print(c, n, color)
            bag[color] = max(bag[color], int(n))
    return bag


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    bag = {'red': 12, 'green': 13, 'blue': 14}

    s1, s2 = 0, 0
    for line in text:
        i, game = line.split(": ")
        i = int(i.split()[-1])
        game = parse(game)
        if all(game[color] <= bag[color] for color in game):
            s1 += i
        s2 += np.product(list(game.values()))

    pone = s1
    print(f"AOC {year} day {day}  Part One: {pone}")

    ptwo = s2
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
