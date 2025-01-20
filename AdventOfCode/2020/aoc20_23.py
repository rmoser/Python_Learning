# Advent of Code
from wsgiref.validate import header_re

year = 2020
day = 23

import numpy as np
import aocd
import os
from pprint import pprint
import itertools as it
import utils
import collections

# os.environ["AOC_SESSION"] = "53616c7465645f5ffc80017c3c8c930fbc4880b09a0cbad8a01217c74864308b01c260ef4e14a659e630448499f917ddbd11b3c5b308647c43be75ef54a40d08"
os.environ["AOC_SESSION"] = "53616c7465645f5f7538531ba6a69f289dbd96f1fdc096ca925f2ca6c250bf6987a1d4d1dedc3d335d639450a7bab765d33fc06d52ed3465933b76a92966b4e0"

text0 = """389125467"""
text1 = aocd.get_data(day=day, year=year)

DEBUG = False

class LinkedList3:
    def __init__(self):
        self.array = np.zeros(shape=1000001, dtype=int)

    def __repr__(self):
        i = self.head
        s = f'({i})'
        for _ in range(15):
            i = self.array[i]
            if i == self.head:
                break
            s += f' {i} '
        return s

    def __iter__(self):
        node = self.head
        while True:
            yield node
            node = self.array[node]
            if node == self.head:
                break

    @property
    def head(self):
        return self.array[0]

    @head.setter
    def head(self, item):
        self.array[0] = item

    @property
    def tail(self):
        return np.argwhere(cups.array == self.head).max()

    @tail.setter
    def tail(self, val):
        self.array[self.tail] = val

    def add(self, val):
        if self.head == 0:
            self.head = val
            self.array[val] = val
            return

        self.array[self.tail] = val
        self.array[val] = self.head


    def add_many(self, items):
        for item in items:
            self.add(item)

    def fill(self, end):
        node = self.tail
        for i in range(self.array.max()+1, end+1):
            self.array[node] = i
            node = i
            if node == end:
                self.array[node] = self.head


    def rot(self):
        self.array[0] = self.array[self.head()]

    def move_3(self):
        s_head = self.array[self.head]
        s_mid = self.array[s_head]
        s_tail = self.array[s_mid]
        self.array[self.head] = self.array[s_tail]  # Cut out the three values

        cut_values = (s_head, s_mid, s_tail)

        # Move three items in LL to after the node with data 'other'
        # Then change head to the next node

        # Find where to insert node (1 less than prev selected value, unless it was in the cut section

        # print(cut_values)
        hi = self.array.max()
        lo = 1
        o = self.head
        while True:
            o -= 1
            if o < lo:
                o = hi
            if o not in cut_values:
                break

        other = self.array[o]  # Where to insert 3 cut nodes

        ### Insert 3 nodes after other
        # Sub list next and prev
        self.array[o] = s_head
        self.array[s_tail] = other
        self.head = self.array[self.head]

        return cut_values, o


class Node2:
    def __init__(self, data, parent=None, next=None, prev=None):
        self.data = data
        self.parent = parent
        self.next = self if next is None else next
        self.prev = self if prev is None else prev

    def __repr__(self):
        return str(self.data)

    def __next__(self):
        return self.next

    def __add__(self, other):
        return self.data + other

    def __sub__(self, other):
        return self.data - other

    def __int__(self):
        return self.data

    def __gt__(self, other):
        return self.data > int(other)

    def __lt__(self, other):
        return self.data < int(other)

    def get_3(self):
        node = self
        for _ in range(3):
            yield node.data
            node = node.next


class LinkedList2:
    def __init__(self):
        self.head = None
        self.__len = 0

    def __repr__(self):
        s = [str(i) for i in self]
        return f'({s[0]}) ' + '  '.join(s[1:])

    def __len__(self):
        return self.__len

    def __iter__(self):
        node = self.head
        while True:
            yield node
            if node.next is self.head:
                break
            node = node.next

    def validate(self):
        n = self.head
        p = n
        err = []
        while True:
            if n.next.prev is not n:
                print(f'Bad next ref: {n}.next.prev is {n.next.prev}')
                err.append((n, 'next'))
            if p.prev.next is not p:
                print(f'Bad prev ref: {p}.prev.next is {p.prev.next}')
                err.append((p, 'prev'))
            n = n.next
            p = p.prev
            if n is self.head or p is self.head.prev:
                break

        return err

    def add(self, data):
        node = Node2(data, self)
        if not self.head:
            self.head = node
            node.next = node
            node.prev = node
            return
        tail = self.head.prev
        node.prev = tail
        node.next = self.head
        tail.next = self.head.prev = node
        self.__len += 1

    def add_many(self, iterable):
        for i in iterable:
            self.add(i)

    def rot(self, n=1):
        if n < 0:
            return self.rot_rev(-n)
        for _ in range(n):
            self.head = self.head.next

    def rot_rev(self, n=1):
        if n < 0:
            return self.rot(-n)
        for _ in range(n):
            self.head = self.head.prev

    def move_3(self):
        # Move three items in LL to after the node with data 'other'
        # Then change head to the next node

        # New UN-linked sub-list needs s_head and s_tail references
        s_head = self.head.next
        s_tail = s_head.next.next

        # Remove first 3 nodes from LinkedList
        self.head.next = s_tail.next  # Updates head.next: Half of the cut
        s_tail.next.prev = self.head  # Updates tail.prev: Cut is complete

        # Find where to insert node (1 less than prev selected value, unless it was in the cut section
        cut_values = set(s_head.get_3())
        # print(cut_values)
        hi = max(self)
        lo = min(self)
        o = self.head
        while True:
            o -= 1
            if o < lo:
                o = hi
            if o not in cut_values:
                break

        other = self.find(o)  # Where to insert 3 cut nodes

        ### Insert 3 nodes after other
        # Sub list next and prev
        s_head.prev = other
        s_tail.next = other.next
        # Main list next and prev
        other.next.prev = s_tail
        other.next = s_head

        self.head = self.head.next

        return cut_values, o
        
    def find(self, value):
        if isinstance(value, Node2):
            return value
        a = self.head
        b = self.head.prev
        while True:
            if a.data == value:
                return a
            if b.data == value:
                return b

            a = a.next
            b = b.prev

            if b is self.head or a is self.head.prev:
                return


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __repr__(self):
        return str(self.data)

    def __next__(self):
        return self.next

    def __add__(self, other):
        return self.data + other

    def __sub__(self, other):
        return self.data - other

    def __int__(self):
        return self.data

    def __gt__(self, other):
        return self.data > int(other)

    def __lt__(self, other):
        return self.data < int(other)

    def get_3(self):
        node = self
        for _ in range(3):
            yield node.data
            if node:
                node = node.next


class LinkedList:
    def __init__(self):
        self.head = None

    def __repr__(self):
        s = [str(i) for i in self]
        return f'({s[0]}) ' + '  '.join(s[1:])

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next

    def append(self, node):
        if self.head is None:
            self.head = node
        else:
            self.tail().next = node

    def add(self, data):
        new = Node(data)
        if not self.head:
            self.head = new
        else:
            node = self.tail()
            node.next = new
        return new

    def add_many(self, iterable):
        node = None
        for i in iterable:
            if node is None:
                node = self.add(i)
            else:
                node.next = Node(i)
                node = node.next

    def pop(self):
        if self.head is None:
            return None
        node = self.head
        self.head = node.next
        node.next = None
        return node

    def rot(self):
        tail = self.tail()
        tail.next = self.pop()

    def tail(self):
        node = self.head
        if not node:
            return None
        while node.next is not None:
            node = node.next
        return node

    def move_3(self):
        # Move three items in LL to after the node with data 'other'
        # Then change head to the next node

        # Pop 3 nodes from LinkedList
        o = self.head
        self.rot()
        s_head = self.pop()
        s_head.next = self.pop()
        s_tail = s_head.next.next = self.pop()

        # Find where to insert node (1 less than prev selected value, unless it was in the cut section
        cut_values = set(int(x) for x in (s_head, s_head.next, s_tail))
        # print(cut_values)
        hi = max(self)
        lo = min(self)
        while True:
            o -= 1
            if o < lo:
                o = hi
            if o not in cut_values:
                break

        other = self.find(o)  # Where to insert 3 cut nodes

        ### Insert 3 nodes after other
        # Sub list next and prev

        s_tail.next = other.next
        other.next = s_head

        return cut_values, o

    def find(self, value):
        if isinstance(value, Node):
            return value
        a = self.head
        while a is not None:
            if a.data == value:
                return a

            a = a.next

    def get(self, n):
        if not self.head:
            return None
        node = self.head
        for _ in range(n):
            if node is None:
                return
            yield node
            node = node.next

def run(cup_list, moves):
    if isinstance(cup_list, (LinkedList, LinkedList2, LinkedList3)):
        cups = cup_list
    else:
        cups = LinkedList()
        cups.add_many(cup_list)

    threshold = 100
    threshold_inc = 100
    threshold_next = 1000
    for i in range(1, moves+1):
        if i == threshold:
            print(f'\rCycle {i}...', end='\t\t\t')
            threshold += threshold_inc
            if threshold == threshold_next:
                threshold_inc *= 10
                threshold_next *= 10

        if DEBUG:
            print(f'\n-- move {i} --')
            print(f'cups: {str(cups)[:60]}')

        pick, next_lower = cups.move_3()

        if DEBUG:
            print(f'pick up: {pick}')
            print(f'destination: {next_lower}')

    print()
    return cups



if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text1
    text = text.strip().splitlines()
    _cups = [int(c) for c in text[0]]

    if False:
        cups = LinkedList()
        cups.add_many(_cups)
        self = cups

    else:
        cups = LinkedList3()
        cups.add_many(_cups)
        cups = run(_cups, 100)

        while int(cups.head) != 1:
            cups.rot()

        pone = ''.join(str(x) for x in list(cups)[1:])
        print(f"AOC {year} day {day}  Part One: {pone}")

        cups = LinkedList3()
        cups.add_many(_cups)
        cups.fill(1000000)
        run(cups, 10000000)

        # cups = run(_cups + list(range(10, 1000000)), 10000000)
        # c = cups.find(1)
        # if c.next is None or c.next.next is None:
        #     cups.rot()
        #     cups.rot()

        i1 = cups.array[1]

        ptwo = i1 * cups.array[i1]
        print(f"AOC {year} day {day}  Part Two: {ptwo}")
