from ps3_hangman import *


def test_isWordGuessed():
    assert isWordGuessed('abc', ['a', 'b', 'c', 'd'])
    assert not isWordGuessed('abc', ['a', 'c'])

def test_getGuessedWord():
    assert getGuessedWord('abc', ['a', 'b', 'c']) == 'abc'
    assert getGuessedWord('abc', ['a', 'c']) == 'a_ c'

def test_getAvailableLetters():
    assert getAvailableLetters('abc') == 'defghijklmnopqrstuvwxyz'
    assert getAvailableLetters('abcdef') == 'ghijklmnopqrstuvwxyz'
