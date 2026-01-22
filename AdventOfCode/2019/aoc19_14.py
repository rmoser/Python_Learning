# Advent of Code
year = 2019
day = 14

import numpy as np
import aocd
import math

text0 = """
10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL
"""
text0 = """
9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL
"""
text0 = """157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT
"""
text0 = """
2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF
"""
text0 = """
171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX
"""
text1 = aocd.get_data(day=day, year=year)


class Ratio(object):
    def __init__(self, name: str, qty: int, ingredients: tuple[tuple[str, int], ...]):
        self.name = name
        self.qty = qty
        self.ready = False
        self.ingredients = dict()
        self.others = dict()
        for name, qty in ingredients:
            self.ingredients[name] = qty

    def __str__(self) -> str:
        s = f"Ratio {self.name}: {self.qty}"
        for k, v in self.ingredients.items():
            s += f"\n\t{k}: {v}"
        return s

    def __repr__(self):
        return self.__str__()

    def req(self):
        return self.ingredients.copy()

    def check_ready(self):
        if not self.others:
            self.ready = True
            return
        if all(other.ready for other in self.others.values()):
            self.ready = True


class Recipe(object):
    def __init__(self, recipes: str):
        self.recipes_input = recipes
        self.recipes = dict()
        self.parse_recipes_input()  # Populates self.recipes
        self.link_recipes()
        self.check_ready()

    def __str__(self):
        return '\n'.join((str(recipe) for recipe in self.recipes.values()))

    def __repr__(self):
        return self.__str__()

    def parse_pair_string(self, pair_string: str) -> tuple[str, int]:
        qty, name = pair_string.split(' ')
        qty = int(qty)
        return name, qty

    def parse_recipes_input(self) -> None:
        for line in self.recipes_input.splitlines():
            ins, outs = line.split(' => ')

            outs = self.parse_pair_string(outs)
            ins = tuple([self.parse_pair_string(i) for i in ins.split(', ')])
            self.recipes[outs[0]] = Ratio(outs[0], outs[1], ins)

    def link_recipes(self) -> None:
        for recipe in self.recipes.values():
            for k in recipe.ingredients.keys():
                if k not in self.recipes:
                    continue
                self.recipes[k].others[recipe.name] = recipe

    def check_ready(self) -> None:
        for recipe in self.recipes.values():
            recipe.check_ready()

    def get_cost(self, out, qty=1):
        d = dict()
        if out not in self.recipes:
            return None

        to_process = [out]
        while to_process:
            name = to_process.pop(0)
            recipe = self.recipes[name]
            recipe.check_ready()
            if not recipe.ready:
                if name not in to_process:
                    to_process.append(name)
                continue

            if name in d:
                qty = d[name]
            q = recipe.qty
            amt = math.ceil(qty / q)

            for k, v in recipe.req().items():
                d[k] = d.get(k, 0) + v * amt
                if k != "ORE":
                    if k not in to_process:
                        to_process.append(k)
            if name in d:
                d.pop(name)

            recipe.check_ready()
            print(name, d, '\n', recipe)

#        print(name, d)
        return d["ORE"]


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip()

    recipes = Recipe(text)

    #print(recipes)

    print(recipes.get_cost("FUEL"))

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
