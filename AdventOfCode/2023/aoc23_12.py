# Advent of Code
year = 2023
day = 12

import numpy as np
import aocd

text0 = """
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""
text1 = aocd.get_data(day=day, year=year)

def brute(record, score):
    if sum(score) + len(score) - 1 == len(record):
        return 1
    return 99999


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text0
    text = text.strip().splitlines()

    for line in text:
        record, score = line.split()
        record = record.strip('.')
        score = [int(i) for i in score.split(',')]

        while record[0] == '#':
            record = record[score[0]+1:]
            score.pop(0)
            record = record.strip('.')
            print(record, score)

        while record[-1] == '#':
            record = record[:score[-1]]
            score.pop(-1)
            record = record.strip('.')
            print(record, score)

        break

    print(record, score)


    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
