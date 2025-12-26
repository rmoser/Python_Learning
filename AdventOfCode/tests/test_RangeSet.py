import pytest
from utils import RangeSet


def test_rangeset_null():
    rs = RangeSet()
    assert rs.lo is None
    assert rs.hi is None
    assert rs.head is None
    assert rs.tail is None
    for i in range(5):
        assert i not in rs
    assert len(rs) == 0

def test_rangeset_lt():
    rs0 = RangeSet(lo=1, hi=8)
    rs1 = RangeSet(lo=10, hi=10)

    assert rs0 < rs1

def test_rangeset_le():
    rs0 = RangeSet(lo=1, hi=9)
    rs1 = RangeSet(lo=10, hi=10)

    assert rs0 <= rs1

def test_rangeset_le_1():
    rs0 = RangeSet(lo=1, hi=10)
    rs1 = RangeSet(lo=10, hi=10)

    assert rs0 <= rs1

def test_rangeset_gt():
    rs0 = RangeSet(lo=1, hi=8)
    rs1 = RangeSet(lo=10, hi=10)

    assert rs1 > rs0

def test_rangeset_ge_0():
    rs0 = RangeSet(lo=1, hi=9)
    rs1 = RangeSet(lo=10, hi=10)

    assert rs1 >= rs0

def test_rangeset_ge_1():
    rs0 = RangeSet(lo=1, hi=10)
    rs1 = RangeSet(lo=10, hi=10)

    assert rs1 >= rs0

def test_rangeset_or_0():
    rs0 = RangeSet(lo=1, hi=9)
    rs1 = RangeSet(lo=10, hi=10)
    rs = rs0 | rs1
    assert rs.lo == 1
    assert rs.hi == 10
    assert rs.head is None
    assert rs.tail is None

def test_rangeset_in():
    rs = RangeSet(lo=1, hi=9)
    assert 0 not in rs
    assert 1 in rs
    assert 9 in rs
    assert 10 not in rs

def test_rangeset_or_1():
    rs0 = RangeSet(lo=1, hi=5)
    rs1 = RangeSet(lo=10, hi=10)
    rs = rs0 | rs1
    assert rs.lo == 1
    assert rs.hi == 5
    assert rs.head is None
    assert rs is rs0
    assert rs.tail is rs1

    assert 1 in rs
    assert 5 in rs
    assert 6 not in rs
    assert 9 not in rs
    assert 10 in rs
    assert 11 not in rs

def test_rangeset_in_many():
    rs = RangeSet(lo=0, hi=0)

    for i in range(0, 100, 2):  # Sparse RangeSet of only even numbers
        rs | RangeSet(lo=i, hi=i)

    for i in range(100): # Verify only even numbers are in
        assert (i in rs) != bool(i % 2)
