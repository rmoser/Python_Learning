from __future__ import annotations

class RangeSet(object):
    def __init__(self, lo: int, hi: int, head: RangeSet = None, tail: RangeSet = None):
        super().__init__()
        self.head = head
        self.tail = tail
        self.lo = lo
        self.hi = hi

    def __repr__(self):
        return f'{'+' if self.head is not None else ''}RangeSet({self.lo}, {self.hi}){'-' if self.tail is not None else ''}'

    def __gt__(self, other):
        return self.lo > other.hi+1

    def __ge__(self, other):
        return other.lo <= self.lo <= other.hi+1 and other.hi <= self.hi

    def __lt__(self, other):
        return self.hi < other.lo-1

    def __le__(self, other):
        return self.lo <= other.lo <= self.hi <= other.hi

    def __eq__(self, other):
        return self.lo <= other.lo and other.hi <= self.hi

    def __ne__(self, other):
        return self.lo > other.hi+1 or self.hi < other.lo-1

    def __or__(self, other):
        if self < other:  # other right of self.  Pass to tail.
            if self.tail is not None:
                return self.tail | other
            else:
                self.tail = other
                other.head = self

        elif self > other:  # other is left of self.  Insert before self in linked list
            self.insert_before(other)

        else:  # Overlapping, extend self to include other
            self.lo = min(self.lo, other.lo)
            self.hi = max(self.hi, other.hi)

            if other is self.tail:
                self.tail = other.tail
            if not self.tail is None:
                self.tail.head = self
                self | self.tail

        return self.find_head()

    def find_head(self):
        if self.head is None:
            return self
        return self.head.find_head()

    def __contains__(self, item: int) -> bool:
        if self.lo <= item <= self.hi:
            return True
        elif self.tail:
            return item in self.tail
        return False

    def __copy__(self):
        return RangeSet(self.lo, self.hi, self.head, self.tail)

    def copy(self):
        return self.__copy__()

    def insert_before(self, other):
        other.head = self.head
        other.tail = self
        if self.head is not None:
            self.head.tail = other
        self.head = other

    def show_all(self):
        return str(self) + (self.tail.show_all() if self.tail is not None else '')

    def __len__(self):
        return self.hi - self.lo + 1 + (len(self.tail) if self.tail is not None else 0)
