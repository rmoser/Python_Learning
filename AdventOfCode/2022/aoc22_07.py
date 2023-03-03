# Advent of Code
year = 2022
day = 7

import numpy as np
import aocd

text0 = """
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""

text1 = aocd.get_data(day=day, year=year)


class Path(object):
    directory = dict()

    def __init__(self, filename: str, size: int = 0, isdir: bool = True, parent=None):
        self.name = filename

        if isinstance(size, int):
            self.size = size
            self.full_size = size
        else:
            self.size = 0
            self.full_size = 0

        self.isdir = isdir

        if isinstance(parent, Path):
            self.parent = parent
            parent.children[filename] = self
            self.fullpath = self.parent.fullpath + tuple(filename)

        else:
            self.parent = None
            self.fullpath = tuple(filename)

        self.children = dict()

        type(self).directory[self.fullpath] = self
        if self.size:
            self.parent.update()

    def __str__(self):
        s = f'\nname: {self.name}   type: {"dir" if self.isdir else "file"}'
        s += f'\n  fullpath: {self.fullpath}'
        if self.isdir:
            s += f'\n  size: {self.full_size} -> n children: {len(self.children)}'
        else:
            s += f'\n  size: {self.size}'
        return s

    def __repr__(self):
        return str(self).replace('\n', '  ')

    def update(self):
        x = self.full_size
        self.full_size = self.size + sum(x.full_size for x in self.children.values())
        if x != self.full_size and self.parent:
            self.parent.update()


def scan(text, path=None) -> Path:
    #  Name, IsDir, Contents, Parent
    curdir: (Path, None) = None
    for l, line in enumerate(text):
        # print(f"{l}: '{line}'")
        if len(line) < 2:
            continue

        if line[0] == '$':
            cmd = line.split()
            if cmd[1] == 'cd':
                arg = cmd[2]
                if arg == '/':
                    directory = Path('/')
                    curdir = directory  # Root dir
                elif arg == '..':
                    curdir = curdir.parent  # Parent dir
                else:
                    # Find sub dir with this name
                    curdir = curdir.children[arg]

        else:
            # ls output
            a, b = line.split()
            if a == 'dir':
                # print(f'new dir: {b} in {curdir.__repr__()}')
                # Found a new directory
                new = Path(b, parent=curdir)

            else:
                # print(f'new file: {b} size {a} in {curdir}')
                new = Path(b, size=int(a), isdir=False, parent=curdir)

    return directory


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()

    root = scan(text)

    pone = sum(d.full_size for d in root.directory.values() if d.full_size <= 100000 and d.isdir)

    space_required = 30000000
    space_available = 70000000 - root.full_size
    space_delete = space_required - space_available

    d = dict()
    for k, v in root.directory.items():
        if v.isdir and v.full_size > space_delete:
            d[v.full_size - space_delete] = v

    x = min(d.keys())
    ptwo = d[x].full_size

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
