# Advent of Code
year = 2021
day = 21

import numpy as np
import aocd

text0 = """
Player 1 starting position: 4
Player 2 starting position: 8
"""

text1 = aocd.get_data(day=day, year=year)

iter_100 = 0
iter_100_count = 0


def roll_100():
    global iter_100, iter_100_count
    iter_100 += 1
    iter_100_count += 1
    if iter_100 > 100:
        iter_100 = 1
    return iter_100


dd = np.array([0, 0, 0, 1, 3, 6, 7, 6, 3, 1], dtype=int)

dirac_dist = np.array([
    #0  1  2  3  4  5  6  7  8  9
    [0, 1, 3, 6, 7, 6, 3, 1, 0, 0],
    [0, 0, 1, 3, 6, 7, 6, 3, 1, 0],
    [0, 0, 0, 1, 3, 6, 7, 6, 3, 1],
    [1, 0, 0, 0, 1, 3, 6, 7, 6, 3],
    [3, 1, 0, 0, 0, 1, 3, 6, 7, 6],
    [6, 3, 1, 0, 0, 0, 1, 3, 6, 7],
    [7, 6, 3, 1, 0, 0, 0, 1, 3, 6],
    [6, 7, 6, 3, 1, 0, 0, 0, 1, 3],
    [3, 6, 7, 6, 3, 1, 0, 0, 0, 1],
    [1, 3, 6, 7, 6, 3, 1, 0, 0, 0]
]).T

# score_dist = np.array([
#     #0  1  2  3  4  5  6  7  8  9
#     [0, 0, 3, 7, 3, 0, 0, 3, 7, 3, 0],
#     [0, 0, 1, 6, 6, 1, 0, 1, 6, 6, 1],
#     [0, 0, 0, 3, 7, 3, 0, 0, 3, 7, 3],
#     [0, 1, 0, 1, 6, 6, 1, 0, 1, 6, 6],
#     [0, 3, 0, 0, 3, 7, 3, 0, 0, 3, 7],
#     [0, 6, 1, 0, 1, 6, 6, 1, 0, 1, 6],
#     [0, 7, 3, 0, 0, 3, 7, 3, 0, 0, 3],
#     [0, 6, 6, 1, 0, 1, 6, 6, 1, 0, 1],
#     [0, 3, 7, 3, 0, 0, 3, 7, 3, 0, 0],
#     [0, 1, 6, 6, 1, 0, 1, 6, 6, 1, 0]
# ]).T

scores
score_dist = diract_dist * scores

def update(arr):
    # pos_temp[i] = (pos_temp[i] * np.identity(n)).dot(dirac_dist)
    wins = np.array([0, 0])
    new = np.zeros(arr.shape, dtype=np.int64)
    for i in range(2):
        for p in range(10):
            for c in range(999, -1, -1):
                new[i, p, c:c+11] += arr[i, p, c] * score_dist[p]
        new[1-i] *= 27

        _wins = np.atleast_2d(new[i, :, 1000:].sum(axis=0)).T
        wins[i] = _wins.sum()
        new[i, :, 1000:] = 0
        new[1-i, :, :] -= _wins

    return new, wins




    # print("After: ", score_arr)
    # print("After: ", score_update_arr)
    # print(0, np.convolve(score_arr[0], score_update_arr[0]))
    # print(1, np.convolve(score_arr[1], score_update_arr[1]))
    # print(result)

    return


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text0
    text = text.strip().splitlines()
    player_pos = [int(line.split()[-1]) for line in text]
    player_score = [0, 0]

    print(player_pos)

    iter = 0
    while True:
        # print(iter)
        # print(player_pos)
        # print(player_score)
        iter += 1

        player_pos[0] += roll_100() + roll_100() + roll_100()
        player_pos[0] = 1 + ((player_pos[0] - 1) % 10)

        player_score[0] += player_pos[0]
        if player_score[0] >= 1000:
            break

        player_pos[1] += roll_100() + roll_100() + roll_100()
        player_pos[1] = 1 + ((player_pos[1] - 1) % 10)

        player_score[1] += player_pos[1]
        if player_score[1] >= 1000:
            break

    pone = min(player_score) * iter_100_count
    print(min(player_score))
    print(iter_100_count)
    print(f"AOC {year} day {day}  Part One: {pone}")


    ###
    ### Part two
    ###

    if True:
        # Data[player, position, score] = Count
        data = np.zeros(shape=(2, 10, 1010), dtype=np.int64)
        for p, n in enumerate([np.int64(line.split()[-1]) for line in text]):
            data[p, n, 0] = 1

    else:
        player_pos = np.zeros(shape=(2, 10), dtype=np.int64)
        player_score = list(np.array([[0, 5, 0], [0, 0, 5]], dtype=np.int64))

        player_pos[0, 0] = 2
        player_pos[0, 5] = 3
        player_pos[1, 1] = 1
        player_pos[1, 7] = 4

    player_wins = np.array([0, 0], dtype=np.int64)

    iter = 0
    while True:
        iter += 1

        """ To execute for debug:
            score_arr = player_score
            pos_arr = player_pos
        """
        # Update player scores and check win conditions
        data, wins = update(data)
        player_wins += wins

        if data.sum() == 0:
            break

    ptwo = player_wins.max()
    print(f"AOC {year} day {day}  Part Two: {ptwo}")
