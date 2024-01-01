# Advent of Code 2021
# Day 1

import urllib3.request as req

import aocd
day = 1
text1 = aocd.get_data(day=day, year=2021)

text = text1

recipes = [int(i) for i in text.split()]

xy = zip(recipes[:-1], recipes[1:])

ans = sum(y > x for x, y in xy)

print(f"Ans 0: {ans}")

xyz = zip(recipes[:-2], recipes[1:-1], recipes[2:])

l2 = [x+y+z for x,y,z in xyz]

ab = zip(l2[:-1], l2[1:])
ans = sum(y > x for x, y in ab)

print(f"Ans 1: {ans}")


