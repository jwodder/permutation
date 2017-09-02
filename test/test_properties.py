import pytest
from   permutation import Permutation

PERMUTATIONS = [
    # Permutation, degree, order, even, sign
    (Permutation.identity(), 0, 1, True, 1),
    (Permutation.transposition(1,2), 2, 2, False, -1),
    (Permutation.transposition(2,1), 2, 2, False, -1),
    (Permutation.transposition(2,3), 3, 2, False, -1),
    (Permutation.cycle(1,3,2), 3, 3, True, 1),
    (Permutation.cycle(1,2,3), 3, 3, True, 1),
    (Permutation.transposition(1,3), 3, 2, False, -1),
    (Permutation.transposition(3,4), 4, 2, False, -1),
    (Permutation.from_cycles((1,2),(3,4)), 4, 2, True, 1),
    (Permutation.cycle(1,2,3,4), 4, 4, False, -1),
    (Permutation.from_cycles((1,2,3),(4,5)), 5, 6, False, -1),
    (Permutation.cycle(1,2,3,4,5), 5, 5, True, 1),
    (Permutation.from_cycles((1,2),(3,4),(5,6)), 6, 2, False, -1),
    (Permutation.from_cycles((1,2,3,4),(5,6)), 6, 4, True, 1),
    (Permutation.from_cycles((1,2,3),(4,5,6)), 6, 3, True, 1),
    (Permutation.cycle(1,2,3,4,5,6), 6, 6, False, -1),
]


@pytest.mark.parametrize('p,degree', [
    (p, degree) for p, degree, _, _, _ in PERMUTATIONS
])
def test_degree(p, degree):
    assert p.degree == degree

@pytest.mark.parametrize('p,order', [
    (p, order) for p, _, order, _, _ in PERMUTATIONS
])
def test_order(p, order):
    assert p.order == order

@pytest.mark.parametrize('p,even', [
    (p, even) for p, _, _, even, _ in PERMUTATIONS
])
def test_is_even(p, even):
    assert p.is_even is even

@pytest.mark.parametrize('p,even', [
    (p, even) for p, _, _, even, _ in PERMUTATIONS
])
def test_is_odd(p, even):
    assert p.is_odd is (not even)

@pytest.mark.parametrize('p,sign', [
    (p, sign) for p, _, _, _, sign in PERMUTATIONS
])
def test_sign(p, sign):
    assert p.sign == sign
