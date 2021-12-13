# Advent of Code
year = 2021
day = 8

import numpy as np
import aocd
from itertools import permutations

text0 = """
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
"""

text1 = aocd.get_data(day=day, year=year)

text_ans = open("aoc21_08_ans.txt", 'r').read()

def digit(s, d):
    if len(s) == 2:
        i = set(s)
        d[1] = i
        d["".join(sorted(i))] = 1
        return 1
    if len(s) == 4:
        i = set(s)
        d[4] = i
        d["".join(sorted(i))] = 4
        return 4
    if len(s) == 3:
        i = set(s)
        d[7] = i
        d["".join(sorted(i))] = 7
        return 7
    if len(s) == 7:
        i = set(s)
        d[8] = i
        d["".join(sorted(i))] = 8
        return 8
    if len(s) == 5:  # 2 3 5
        return None
    if len(s) == 6:  # 0 6 9
        return None


if __name__ == '__main__':
    if False:

        segments = {
            1: "cf",
            7: "acf",
            4: "bcdf",
            8: "abcdefg",

            2: "acdeg",
            3: "acdfg",
            5: "abdfg",

            6: "abdefg",
            9: "abcdfg",
            0: "abcefg",
        }

        lookup = {frozenset(v): str(k) for k, v in segments.items()}
        translations = [str.maketrans("".join(p), "abcdefg") for p in permutations("abcdefg", 7)]
        n = len(translations)

        a = b = 0
        for l, line in enumerate(text1.splitlines()):
            patterns, code = line.split(" | ")
            for part in code.split():
                a += len(part) in {2, 3, 4, 7}

            matches = 0
            for i, t in enumerate(translations):
                if all(frozenset(w.translate(t)) in lookup for w in patterns.split()):
                    # print(f"{i}/{n}", "  ".join([f"{chr(x)}: {chr(t[x])}" for x in t]))
                    # break
                    code = "".join([lookup[frozenset(n.translate(t))] for n in code.split()])
                    # print(code)
                    matches += 1
            print(line, "|", code)
            # b += int(code)

        print("part a:", a)
        print("part b:", b)

    else:
        text = text_ans
        text = text.strip().splitlines()

        # print(text)

        pone = 0
        ptwo = 0
        for t in text:
            digits = dict()
            tup = [x.split() for x in t.split(" | ")]
            if len(tup) == 2:
                ins, outs = tup
                ans = None
            elif len(tup) == 3:
                ins, outs, ans = tup
                ans = int(ans[0])
            else:
                raise ValueError(f"Bad input string: {t}")
            # print(ins_outs, len(ins_outs))

            # Part one says only count on output side
            for s in outs:
                if digit(s, digits) is not None:
                    pone += 1

            for s in ins:
                digit(s, digits)

            # print(f"Digits dict: {digits}")

            one = digits[1]
            four = digits[4]
            seven = digits[7]
            eight = digits[8]

            fives = list()
            for x in ins + outs:  # 2 3 5
                if len(x) == 5:
                    x = set(x)
                    if x not in fives:
                        fives.append(x)

            sixes = list()
            for x in ins + outs:  # 0 6 9
                if len(x) == 6:
                    x = set(x)
                    if x not in sixes:
                        sixes.append(x)

            # Know 0, 1, 4, 7
            # Document known LED indicators as CAPS
            A = digits[7] - digits[1]
            digits['A'] = list(A)[0]

            ADG = fives[0] & fives[1] & fives[2]
            three = ADG | one
            digits[3] = three
            digits["".join(sorted(three))] = 3
            fives.remove(three)  # 2 5

            D = ADG & four
            digits['D'] = list(D)[0]

            B = digits[4] - digits[1] - D
            digits['B'] = list(B)[0]

            G = ADG - A - D
            digits['G'] = list(G)[0]

            # three = digits[7] + D + G
            # digits[3] = three
            # digits["".join(sorted(three))] = 3
            # fives.remove(three)  # 2 5

            nine = three | B
            digits[9] = nine
            digits["".join(sorted(nine))] = 9
            sixes.remove(nine)  # 0 6
            # print(f"after nine - sixes: {sixes}")

            E = eight - nine
            digits['E'] = E

            if sixes[0] - sixes[1] == D:
                six, zero = sixes
            else:
                zero, six = sixes
            sixes.remove(zero)
            sixes.remove(six)
            digits[0] = zero
            digits["".join(sorted(zero))] = 0
            digits["".join(sorted(six))] = 6
            digits[6] = six

            C = zero - six
            digits['C'] = C

            if fives[0] - fives[1] - E == C:
                two, five = fives
            else:
                five, two = fives
            fives.remove(two)
            fives.remove(five)
            digits[2] = two
            digits["".join(sorted(two))] = 2
            digits[5] = five
            digits["".join(sorted(five))] = 5

            # print([(k, digits[k]) for k in digits if type(k) == 'set'])

            # Know all the numbers now
            score = "".join([str(digits["".join(sorted(s))]) for s in outs])
            score = int(score)
            ptwo += score
            print(f"outs: {outs} -> {score}")
            if ans is not None:
                if ans != score:
                    print("]\n\n*** ERROR")
                    print(f"ins : {ins}")
                    print(f"outs: {outs}")
                    print(f"digs: {digits}")
                    print(f"scor: {score}")
                    print(f"ans : {ans}")

                    raise ValueError(f"Failed.")

        print(len(text))
        print(f"AOC {year} day {day}  Part One: {pone}")

        print(f"AOC {year} day {day}  Part Two: {ptwo}")
