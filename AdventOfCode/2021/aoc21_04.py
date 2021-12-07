# Advent of Code 2021
# Day 4

import numpy as np
import aocd
day = 4
text = aocd.get_data(day=day, year=2021)


def mat_check_win(mat):
    for i in range(5):
        if mat[:, i].sum() == -5:
            return True
        if mat[i, :].sum() == -5:
            return True

    # if mat.diagonal().sum() == -5:
    #     return True
    #
    # if np.fliplr(mat).diagonal().sum() == -5:
    #     return True

    return False


def mat_score(mat, n):
    return mat[mat != -1].sum() * n


def mat_update(mat, n):
    mat[mat == n] = -1


if __name__ == '__main__':
    # Read inputs
    arr_string = ""
    numbers = []
    mats = list()

    for i, line in enumerate(text.splitlines()):
        # print(f"{i}: {line}")
        if "," in line:
            numbers = list(map(int, line.split(',')))
            print(f"nums: {numbers}")
            continue

        if len(line):
            arr_string += " " + line

        if len(arr_string) >= 75:
            mat = np.array(arr_string.split()).astype(int).reshape((5, 5))
            mats.append(mat)
            arr_string = ""

    print(f"N cards: {len(mats)}")

    # Play bingo

    winners = np.zeros(len(mats), dtype=int)
    winners.fill(len(mats))

    scores = np.zeros(len(mats), dtype=int)

    for r, n in enumerate(numbers):
        print(f"Round {r}: n={n}")
        # _ = [print(f"\n{mat}") for mat in mats]

        for i, mat in enumerate(mats):
            if mat is not None:
                mat_update(mat, n)
                if mat_check_win(mat):
                    print(f"Card {i} WON!\n{mat}")
                    winners[i] = r
                    print(winners)
                    scores[i] = mat_score(mat, n)
                    # print(f"\nRound {r}: Player {i} won on {n}.  Score: {mat_score(mat, n)}")
                    mats[i] = None
                    # # _ = [print(f"\n{mat}") for mat in mats]

        #input("press enter")

    print("\n\nPart one:")
    winner = winners.argmin()
    print(f"Best Bingo card: {winner}  Score: {scores[winner]}")

    print("\n\nPart two:")
    loser = winners.argmax()
    print(f"Worst Bingo card: {loser}  Score: {scores[loser]}")
