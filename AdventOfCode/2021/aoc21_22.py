# Advent of Code
year = 2021
day = 22

import numpy as np
import aocd
import itertools

texta = '''
on x=0..2,y=0..1,z=0..1
off x=1..2,y=0..1,z=0..1
'''

text00 = """
on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10
"""

text01 = """
on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
"""

text02 = """
on x=-5..47,y=-31..22,z=-19..33
on x=-44..5,y=-27..21,z=-14..35
on x=-49..-1,y=-11..42,z=-10..38
on x=-20..34,y=-40..6,z=-44..1
off x=26..39,y=40..50,z=-2..11
on x=-41..5,y=-41..6,z=-36..8
off x=-43..-33,y=-45..-28,z=7..25
on x=-33..15,y=-32..19,z=-34..11
off x=35..47,y=-46..-34,z=-11..5
on x=-14..36,y=-6..44,z=-16..29
on x=-57795..-6158,y=29564..72030,z=20435..90618
on x=36731..105352,y=-21140..28532,z=16094..90401
on x=30999..107136,y=-53464..15513,z=8553..71215
on x=13528..83982,y=-99403..-27377,z=-24141..23996
on x=-72682..-12347,y=18159..111354,z=7391..80950
on x=-1060..80757,y=-65301..-20884,z=-103788..-16709
on x=-83015..-9461,y=-72160..-8347,z=-81239..-26856
on x=-52752..22273,y=-49450..9096,z=54442..119054
on x=-29982..40483,y=-108474..-28371,z=-24328..38471
on x=-4958..62750,y=40422..118853,z=-7672..65583
on x=55694..108686,y=-43367..46958,z=-26781..48729
on x=-98497..-18186,y=-63569..3412,z=1232..88485
on x=-726..56291,y=-62629..13224,z=18033..85226
on x=-110886..-34664,y=-81338..-8658,z=8914..63723
on x=-55829..24974,y=-16897..54165,z=-121762..-28058
on x=-65152..-11147,y=22489..91432,z=-58782..1780
on x=-120100..-32970,y=-46592..27473,z=-11695..61039
on x=-18631..37533,y=-124565..-50804,z=-35667..28308
on x=-57817..18248,y=49321..117703,z=5745..55881
on x=14781..98692,y=-1341..70827,z=15753..70151
on x=-34419..55919,y=-19626..40991,z=39015..114138
on x=-60785..11593,y=-56135..2999,z=-95368..-26915
on x=-32178..58085,y=17647..101866,z=-91405..-8878
on x=-53655..12091,y=50097..105568,z=-75335..-4862
on x=-111166..-40997,y=-71714..2688,z=5609..50954
on x=-16602..70118,y=-98693..-44401,z=5197..76897
on x=16383..101554,y=4615..83635,z=-44907..18747
off x=-95822..-15171,y=-19987..48940,z=10804..104439
on x=-89813..-14614,y=16069..88491,z=-3297..45228
on x=41075..99376,y=-20427..49978,z=-52012..13762
on x=-21330..50085,y=-17944..62733,z=-112280..-30197
on x=-16478..35915,y=36008..118594,z=-7885..47086
off x=-98156..-27851,y=-49952..43171,z=-99005..-8456
off x=2032..69770,y=-71013..4824,z=7471..94418
on x=43670..120875,y=-42068..12382,z=-24787..38892
off x=37514..111226,y=-45862..25743,z=-16714..54663
off x=25699..97951,y=-30668..59918,z=-15349..69697
off x=-44271..17935,y=-9516..60759,z=49131..112598
on x=-61695..-5813,y=40978..94975,z=8655..80240
off x=-101086..-9439,y=-7088..67543,z=33935..83858
off x=18020..114017,y=-48931..32606,z=21474..89843
off x=-77139..10506,y=-89994..-18797,z=-80..59318
off x=8476..79288,y=-75520..11602,z=-96624..-24783
on x=-47488..-1262,y=24338..100707,z=16292..72967
off x=-84341..13987,y=2429..92914,z=-90671..-1318
off x=-37810..49457,y=-71013..-7894,z=-105357..-13188
off x=-27365..46395,y=31009..98017,z=15428..76570
off x=-70369..-16548,y=22648..78696,z=-1892..86821
on x=-53470..21291,y=-120233..-33476,z=-44150..38147
off x=-93533..-4276,y=-16170..68771,z=-104985..-24507
"""

text1 = aocd.get_data(day=day, year=year)


class Rect:
    def __init__(self, c0, c1):
        self.c = np.array([c0, c1], dtype=np.longlong)
        self.c0 = tuple(self.c.min(axis=0))
        self.c1 = tuple(self.c.max(axis=0))

        self._shape = tuple(np.abs(np.diff(self.c, axis=0)).flatten())
        self.corners = frozenset(itertools.product(*self.c.T))
        self.volume = np.product(np.array(self._shape) + 1)

    def __contains__(self, other):
        if isinstance(other, tuple):
            return all(self.c0[i] <= other[i] <= self.c1[i] for i in range(3))
        elif isinstance(other, Rect):
            return all(c in self for c in other.corners)
        raise TypeError("contains() requires a Coordinate as tuple (x,y,z) or a Rect object")

    def __hash__(self):
        return self.corners.__hash__()

    def __eq__(self, other):
        return self.corners == other.corners

    def contains(self, other):
        # To check only the x-axis, send a tuple with only x value: (x, None, None)
        result = False
        if isinstance(other, tuple):
            result = [c is None or (self.c0[i] <= c <= self.c1[i]) for i, c in enumerate(other)]
            return all(result), tuple(result)

        elif isinstance(other, Rect):
            result = [self.c0[i] <= other.c0[i] and other.c1[i] <= self.c1[i] for i in range(3)]
            return all(result), tuple(result)

    def intersects(self, other):
        if isinstance(other, tuple):
            result = []
            for i, c in enumerate(other):
                if c is None:
                    continue
                _c = [None, None, None]
                _c[i] = c
                result.append(self.contains(tuple(_c))[0])
            return all(result), tuple(result)

        if isinstance(other, Rect):
            result = []
            for i in range(3):
                _c = [None, None, None]
                _c[i] = other.c0[i]
                a = self.intersects(tuple(_c))[0]

                _c = [None, None, None]
                _c[i] = other.c1[i]
                b = self.intersects(tuple(_c))[0]

                _c = [None, None, None]
                _c[i] = self.c0[i]
                c = other.intersects(tuple(_c))[0]

                _c = [None, None, None]
                _c[i] = self.c1[i]
                d = other.intersects(tuple(_c))[0]

                result.append(a or b or c or d)
            return all(result), tuple(result)

        # raise TypeError("intersect() requires a Rect object")
        raise TypeError(f"intersects() requires a Coordinate as tuple (x,y,z) or a Rect object: {other} is {type(other)}")

    def split(self, other):
        items = [self]
        if all(isinstance(c, int) for c in other) and not self.contains(other)[0]:
            return items
        for i in range(3):
            if other[i] is None:
                continue
            for r in range(len(items)-1, -1, -1):
                it = items.pop(r)
                if it.c0[i] < other[i] <= it.c1[i]:
                    # print("Right split", self.c0, other, self.c1)
                    new_c = list(it.c0)
                    new_c[i] = other[i]+1
                    items.append(Rect(new_c, it.c1))

                    new_c = list(it.c1)
                    new_c[i] = other[i]
                    items.append(Rect(it.c0, new_c))

                elif it.c0[i] <= other[i] < it.c1[i]:
                    # print("Left split", self.c0, other, self.c1)
                    new_c = list(it.c0)
                    new_c[i] = other[i]
                    items.append(Rect(new_c, it.c1))

                    new_c = list(it.c1)
                    new_c[i] = other[i]+1
                    items.append(Rect(it.c0, new_c))

                else:
                    items.append(it)
        return items

    def fracture(self, other):
        if isinstance(other, tuple):
            return self.fracture(Rect(other, other))

        items = [self]

        done = []

        for axis in range(3):
            for r in range(len(items)-1, -1, -1):
                rect = items.pop(r)
                if rect.c0[axis] == rect.c1[axis]:
                    items.append(rect)
                    continue

                new = []
                if rect.c0[axis] < other.c0[axis] <= rect.c1[axis]:  # Other's lower corner overlaps
                    # rect = (0,0,0) (1,0,0)
                    # other.c0 = (0,0,0) (0,0,0)
                    # result = (0,0,0) (0,0,0) + (1,0,0) (1,0,0)

                    # Lower section split
                    c = list(rect.c1)
                    c[axis] = other.c0[axis]-1  # upper corner of lower half
                    # print("First add:", rect.c0, tuple(c))
                    _rect0 = Rect(rect.c0, tuple(c))

                    c = list(rect.c0)
                    c[axis] = other.c0[axis]  # lower corner of upper half
                    _rect1 = Rect(tuple(c), rect.c1)  # Remainder

                    done.append(_rect0)  # Lower slice, not overlapping
                    rect = _rect1  # Remainder to check against the higher corner

                if rect.c0[axis] <= other.c1[axis] < rect.c1[axis]:
                    c = list(rect.c1)
                    c[axis] = other.c1[axis]  # Upper corner of lower half
                    # print("Second add:", rect.c0, tuple(c))
                    _rect0 = Rect(rect.c0, tuple(c))

                    c = list(rect.c0)
                    c[axis] = other.c1[axis]+1
                    _rect1 = Rect(tuple(c), rect.c1)

                    items.append(_rect0)
                    done.append(_rect1)
                    rect = None

                if rect:
                    items.append(rect)

                # print(f"axis: {axis}  r: {rect}, new {new}, items:{items}")

        # print(f"items: {len(items)}, done: {len(done)}")

        total_vol = sum(r.volume for r in done) + items[0].volume
        if total_vol != self.volume:
            raise AssertionError(f"Bad fracture: {self}->{other} volume from {self.volume} to {total_vol}")
        return items, done

    def shape(self):
        return self._shape

    def __str__(self):
        return f"Rect({self.c0}, {self.c1})"

    def __repr__(self):
        return self.__str__()



def apply(inst, arr):
    on, ((x0, xn), (y0, yn), (z0, zn)) = inst

    if any((-50 > c or 50 < c) for c in (x0, xn, y0, yn, z0, zn)):
        return arr, 0

    coords = set(itertools.product(range(x0, xn+1), range(y0, yn+1), range(z0, zn+1)))

    if on:
        new_arr = arr | coords
        return new_arr, len(new_arr - arr)
    else:
        new_arr = arr - coords
        return new_arr, -len(arr - new_arr)


def reduce(rects):
    for a, b in itertools.combinations(rects, 2):
        if sum(a.intersects(b)[1]) < 2:
            continue
        corners = np.array(list(a.corners) + list(b.corners))
        c0 = np.min(corners, axis=0)
        c1 = np.max(corners, axis=0)
        new = Rect(tuple(c0), tuple(c1))
        if new.volume == a.volume + b.volume:
            return reduce(set(rects) - set([a]) - set([b]) | set([new]))

    return rects


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    instructions = [line.split() for line in text]
    parsed_instructions = []
    for line in instructions:
        line[0] = line[0] == 'on'
        xyz = [inst[2:].split("..") for inst in line[1].split(',')]
        line[1] = tuple(tuple(int(i) for i in coord) for coord in xyz)
        line[1] = Rect(*tuple(tuple(x) for x in np.array(line[1]).T))
        # print(line)
        parsed_instructions.append(line)

    _ = [print(i, x) for i, x in enumerate(parsed_instructions)]

    space = []
    for counter, (on, rect) in enumerate(parsed_instructions):
        counter = f"{counter} : {len(parsed_instructions)-1}"

        if not pone and (np.abs(rect.c) > 50).any():
            pone = sum(r.volume for r in space)
            print(f"AOC {year} day {day}  Part One: {pone}")

        if len(space) == 0 and on:
            space.append(rect)
            print(f"STRT iter {counter}, vol {sum(r.volume for r in space)}, space: {space}")
            continue

        if any(r.contains(rect)[0] for r in space) and on:
            # print(f"NOP iter {counter}, vol {sum(r.volume for r in space)}, space: {space}")
            continue

        untouched = []
        touched = []
        for r in space:
            if not rect.intersects(r)[0]:
                untouched.append(r)
                continue
            item, rest = r.fracture(rect)

            touched += rest
        if on:
            touched.append(rect)

        # print(f"PRE  iter {counter}, untouched: {len(untouched)} {sum(r.volume for r in untouched)}, touched: {len(touched)}: {touched}")
        # touched = list(reduce(touched))
        space = untouched + touched
        print(f"POST iter {counter}, vol {sum(r.volume for r in space) if len(space) < 1000 else ''}, touched: {len(touched)}: {touched if len(touched) < 20 else ''}")

    ptwo = sum(r.volume for r in set(space))

    print(f"AOC {year} day {day}  Part One: {pone}")
    print(f"AOC {year} day {day}  Part Two: {ptwo}")

