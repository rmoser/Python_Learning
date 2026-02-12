import pytest
import numpy as np
import aoc19_22 as tgt

N_VALS = (23, 29, 31, 37)
MY_TEXT = '''deal with increment 3
deal into new stack
cut -2846
deal with increment 33
cut -8467
deal into new stack
deal with increment 46
cut 6752
deal with increment 63
deal into new stack
deal with increment 70
deal into new stack
deal with increment 14
cut -1804
deal with increment 68
cut -4936
deal with increment 15
cut -3217
deal with increment 49
cut -1694
deal with increment 58
cut -6918
deal with increment 13
cut -4254
deal with increment 4
deal into new stack
cut 5490
deal into new stack
deal with increment 35
deal into new stack
deal with increment 7
cut 854
deal with increment 46
cut -8619
deal with increment 32
deal into new stack
cut -6319
deal with increment 31
cut 1379
deal with increment 66
cut -7328
deal with increment 55
cut -6326
deal with increment 10
deal into new stack
cut 4590
deal with increment 18
cut -9588
deal with increment 5
cut 3047
deal with increment 24
cut -1485
deal into new stack
deal with increment 53
cut 5993
deal with increment 54
cut -5935
deal with increment 49
cut -3349
deal into new stack
deal with increment 28
cut -4978
deal into new stack
deal with increment 30
cut -1657
deal with increment 50
cut 3732
deal with increment 30
cut 6838
deal with increment 30
deal into new stack
cut -3087
deal with increment 42
deal into new stack
deal with increment 68
cut 3376
deal with increment 51
cut -3124
deal with increment 57
deal into new stack
cut -158
deal into new stack
cut -3350
deal with increment 33
deal into new stack
cut 3387
deal with increment 54
cut 1517
deal with increment 20
cut -3981
deal with increment 64
cut 6264
deal with increment 3
deal into new stack
deal with increment 5
cut 232
deal with increment 29
deal into new stack
cut -5147
deal with increment 51'''

@pytest.mark.parametrize("deck_size", N_VALS)
def test_run__deal_into_new_stack_0(deck_size):
    tgt.text = 'deal into new stack'
    tgt.run.cache_clear()

    for i in range(deck_size):
        assert tgt.run(deck_size, i) == (deck_size - i - 1) % deck_size


@pytest.mark.parametrize("deck_size", N_VALS)
def test_run_rev__deal_into_new_stack_0(deck_size):
    tgt.text = 'deal into new stack'
    tgt.run.cache_clear()
    tgt.run_rev.cache_clear()

    for i in range(deck_size):
        x = tgt.run(deck_size, i)
        assert tgt.run_rev(deck_size, x) == i



@pytest.mark.parametrize("deck_size", N_VALS)
def test_run__cut_n_cards_0(deck_size):
    for j in range(10):
        tgt.text = f'cut {j}'
        tgt.run.cache_clear()

        for i in range(deck_size):
            assert tgt.run(deck_size, i) == (i - j) % deck_size


@pytest.mark.parametrize("deck_size", N_VALS)
def test_run_rev__cut_n_cards_0(deck_size):
    for j in range(10):
        tgt.text = f'cut {j}'
        tgt.run.cache_clear()
        tgt.run_rev.cache_clear()

        for i in range(deck_size):
            x = tgt.run(deck_size, i)
            assert tgt.run_rev(deck_size, x) == i



@pytest.mark.parametrize("deck_size", N_VALS)
def test_run__deal_with_increment_0(deck_size):
    for j in range(1, 10):
        tgt.text = f'deal with increment {j}'
        tgt.run.cache_clear()

        for i in range(deck_size):
            assert tgt.run(deck_size, i) == (i * j) % deck_size


@pytest.mark.parametrize("deck_size", N_VALS)
def test_run_rev__deal_with_increment_0(deck_size):
    for j in range(1, 10):
        tgt.text = f'deal with increment {j}'
        tgt.run.cache_clear()
        tgt.run_rev.cache_clear()

        for i in range(deck_size):
            x = tgt.run(deck_size, i)
            assert tgt.run_rev(deck_size, x) == i


# Complex instruction tests
def test_run__complex_0():
    tgt.text = MY_TEXT
    tgt.run.cache_clear()

    assert tgt.run(10007, 2019) == 7545

def test_run_rev_complex_0():
    tgt.text = MY_TEXT
    tgt.run.cache_clear()
    tgt.run_rev.cache_clear()

    assert tgt.run_rev(10007, 7545) == 2019
