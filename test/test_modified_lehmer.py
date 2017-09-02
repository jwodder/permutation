import pytest
from   permutation import Permutation

MOD_LEHMER = [
    (  0, Permutation.identity()),
    (  1, Permutation.transposition(1,2)),
    (  1, Permutation.transposition(2,1)),
    (  2, Permutation.transposition(2,3)),
    (  3, Permutation.cycle(1,3,2)),
    (  4, Permutation.cycle(1,2,3)),
    (  5, Permutation.transposition(1,3)),
    (  6, Permutation.transposition(3,4)),
    (  7, Permutation.from_cycles((1,2),(3,4))),
    ( 18, Permutation.cycle(1,2,3,4)),
    ( 28, Permutation.from_cycles((1,2,3),(4,5))),
    ( 96, Permutation.cycle(1,2,3,4,5)),
    (127, Permutation.from_cycles((1,2),(3,4),(5,6))),
    (138, Permutation.from_cycles((1,2,3,4),(5,6))),
    (244, Permutation.from_cycles((1,2,3),(4,5,6))),
    (600, Permutation.cycle(1,2,3,4,5,6)),
]

@pytest.mark.parametrize('code,p', MOD_LEHMER)
def test_modified_lehmer(p, code):
    assert p.modified_lehmer() == code

@pytest.mark.parametrize('code,p', MOD_LEHMER)
def test_from_modified_lehmer(p, code):
    assert Permutation.from_modified_lehmer(code) == p
