import pytest

import lib

def test_sum_digits():
    assert lib.sum_digits("0") == 0
    assert lib.sum_digits("1") == 1
    assert lib.sum_digits("2") == 2
    assert lib.sum_digits("3") == 3
    assert lib.sum_digits("4") == 4
    assert lib.sum_digits("5") == 5
    assert lib.sum_digits("6") == 6
    assert lib.sum_digits("7") == 7
    assert lib.sum_digits("8") == 8
    assert lib.sum_digits("9") == 9

    assert lib.sum_digits("00") == 0

    assert lib.sum_digits("a;35d4") == 12
    assert lib.sum_digits("3.14") == 8

    with pytest.raises(ValueError):
        lib.sum_digits("abc")

def test_primes_list():
    assert [] == lib.primes_list(0)
    assert [] == lib.primes_list(1)
    assert [2] == lib.primes_list(2)
    assert [2, 3] == lib.primes_list(3)
    assert [2, 3] == lib.primes_list(4)
    assert [2, 3, 5] == lib.primes_list(5)
    assert [2, 3, 5] == lib.primes_list(6)
    assert [2, 3, 5, 7] == lib.primes_list(7)
    assert [2, 3, 5, 7] == lib.primes_list(8)
    assert [2, 3, 5, 7] == lib.primes_list(9)
    assert [2, 3, 5, 7] == lib.primes_list(10)
    assert [2, 3, 5, 7, 11] == lib.primes_list(11)
    assert [2, 3, 5, 7, 11] == lib.primes_list(11)
    assert [2, 3, 5, 7, 11, 13] == lib.primes_list(13)
    assert [2, 3, 5, 7, 11, 13] == lib.primes_list(14)
    assert [2, 3, 5, 7, 11, 13] == lib.primes_list(15)
    assert [2, 3, 5, 7, 11, 13] == lib.primes_list(16)
    assert [2, 3, 5, 7, 11, 13, 17] == lib.primes_list(17)
    assert [2, 3, 5, 7, 11, 13, 17] == lib.primes_list(18)
    assert [2, 3, 5, 7, 11, 13, 17, 19] == lib.primes_list(19)
    assert [2, 3, 5, 7, 11, 13, 17, 19] == lib.primes_list(20)
    assert [2, 3, 5, 7, 11, 13, 17, 19] == lib.primes_list(21)
    assert [2, 3, 5, 7, 11, 13, 17, 19] == lib.primes_list(22)
    assert [2, 3, 5, 7, 11, 13, 17, 19, 23] == lib.primes_list(23)


def test_uniqueValues():
    assert [] == lib.uniqueValues({})
    assert [] == lib.uniqueValues({1: 1, 2: 1, 3: 1})
    assert [1, 3, 8] == lib.uniqueValues({1: 1, 3: 2, 6: 0, 7: 0, 8: 4, 10: 0})
    assert ["A"] == lib.uniqueValues({"A": 1})
    assert ["A", "B"] == lib.uniqueValues({"A": 1, "B": 2})
    assert ["A", "B"] == lib.uniqueValues({"B": 1, "A": 2})
    assert ["A"] == lib.uniqueValues({"B": 1, "A": 2, "C": 1})


def test_people_0():
    e = lib.Person('eric')
    assert e.say('the sky is blue') == 'eric says: the sky is blue'


def test_people_1():
    le = lib.Lecturer('eric')
    assert le.say('the sky is blue') == 'eric says: the sky is blue'


def test_people_2():
    le = lib.Lecturer('eric')
    assert le.lecture('the sky is blue') == 'I believe that eric says: the sky is blue'


def test_people_3():
    pe = lib.Professor('eric')
    assert pe.say('the sky is blue') == 'eric says: I believe that eric says: the sky is blue'


def test_people_4():
    pe = lib.Professor('eric')
    assert pe.lecture('the sky is blue') == 'I believe that eric says: the sky is blue'


def test_people_5():
    ae = lib.ArrogantProfessor('eric')
    assert ae.say('the sky is blue') == 'eric says: It is obvious that eric says: the sky is blue'


def test_people_6():
    ae = lib.ArrogantProfessor('eric')
    assert ae.lecture('the sky is blue') == 'It is obvious that eric says: the sky is blue'


def test_myDict_0():
    d = lib.myDict()

    d.assign(1, 2)

    assert d.getval(1) == 2

    d.assign(1, 3)

    assert d.getval(1) == 2

def test_myDict_1():
    d = lib.myDict()

    d.assign("A", 1)

    assert d.getval("A") == 1

    with pytest.raises(KeyError):
        d.getval("B")
        d.delete("B")

    d.assign("B", 2)

    assert d.getval("A") == 1
    assert d.getval("B") == 2

    d.delete("A")

    with pytest.raises(KeyError):
        d.getval("A")
        d.delete("A")

    assert d.getval("B") == 2

def test_myDict_2():
    d = lib.myDict()
    d.assign("A", 1)
    assert d.getval("A") == 1
    d.assign("A", 2)
    assert d.getval("A") == 2

