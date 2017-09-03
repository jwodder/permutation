from   collections import namedtuple
import pytest
from   permutation import Permutation

PermData = namedtuple(
    'PermData', 'p degree order even sign mod_lehmer cycles str',
)

PERMUTATIONS = [
    PermData(Permutation.identity(),                     0, 1, True,   1,   0, [],                  '1'),
    PermData(Permutation.transposition(1,2),             2, 2, False, -1,   1, [(1,2)],             '(1 2)'),
    PermData(Permutation.transposition(2,1),             2, 2, False, -1,   1, [(1,2)],             '(1 2)'),
    PermData(Permutation.transposition(2,3),             3, 2, False, -1,   2, [(2,3)],             '(2 3)'),
    PermData(Permutation.cycle(1,3,2),                   3, 3, True,   1,   3, [(1,3,2)],           '(1 3 2)'),
    PermData(Permutation.cycle(1,2,3),                   3, 3, True,   1,   4, [(1,2,3)],           '(1 2 3)'),
    PermData(Permutation.transposition(1,3),             3, 2, False, -1,   5, [(1,3)],             '(1 3)'),
    PermData(Permutation.transposition(3,4),             4, 2, False, -1,   6, [(3,4)],             '(3 4)'),
    PermData(Permutation.from_cycles((1,2),(3,4)),       4, 2, True,   1,   7, [(1,2),(3,4)],       '(1 2)(3 4)'),
    PermData(Permutation.cycle(1,2,3,4),                 4, 4, False, -1,  18, [(1,2,3,4)],         '(1 2 3 4)'),
    PermData(Permutation.from_cycles((1,2,3),(4,5)),     5, 6, False, -1,  28, [(1,2,3),(4,5)],     '(1 2 3)(4 5)'),
    PermData(Permutation.cycle(1,2,3,4,5),               5, 5, True,   1,  96, [(1,2,3,4,5)],       '(1 2 3 4 5)'),
    PermData(Permutation.from_cycles((1,2),(3,4),(5,6)), 6, 2, False, -1, 127, [(1,2),(3,4),(5,6)], '(1 2)(3 4)(5 6)'),
    PermData(Permutation.from_cycles((1,2,3,4),(5,6)),   6, 4, True,   1, 138, [(1,2,3,4),(5,6)],   '(1 2 3 4)(5 6)'),
    PermData(Permutation.from_cycles((1,2,3),(4,5,6)),   6, 3, True,   1, 244, [(1,2,3),(4,5,6)],   '(1 2 3)(4 5 6)'),
    PermData(Permutation.cycle(1,2,3,4,5,6),             6, 6, False, -1, 600, [(1,2,3,4,5,6)],     '(1 2 3 4 5 6)'),
]

@pytest.mark.parametrize('p,degree', [(pd.p, pd.degree) for pd in PERMUTATIONS])
def test_degree(p, degree):
    assert p.degree == degree

@pytest.mark.parametrize('p,order', [(pd.p, pd.order) for pd in PERMUTATIONS])
def test_order(p, order):
    assert p.order == order

@pytest.mark.parametrize('p,even', [(pd.p, pd.even) for pd in PERMUTATIONS])
def test_is_even(p, even):
    assert p.is_even is even

@pytest.mark.parametrize('p,even', [(pd.p, pd.even) for pd in PERMUTATIONS])
def test_is_odd(p, even):
    assert p.is_odd is (not even)

@pytest.mark.parametrize('p,sign', [(pd.p, pd.sign) for pd in PERMUTATIONS])
def test_sign(p, sign):
    assert p.sign == sign

@pytest.mark.parametrize('p,code', [(d.p, d.mod_lehmer) for d in PERMUTATIONS])
def test_modified_lehmer(p, code):
    assert p.modified_lehmer() == code

@pytest.mark.parametrize('p,code', [(d.p, d.mod_lehmer) for d in PERMUTATIONS])
def test_from_modified_lehmer(p, code):
    assert Permutation.from_modified_lehmer(code) == p

@pytest.mark.parametrize('p,cycles', [(d.p, d.cycles) for d in PERMUTATIONS])
def test_to_cycles(p, cycles):
    assert p.to_cycles() == cycles

@pytest.mark.parametrize('p,cycles', [(d.p, d.cycles) for d in PERMUTATIONS])
def test_from_cycles(p, cycles):
    assert Permutation.from_cycles(*cycles) == p

@pytest.mark.parametrize('p,s', [(d.p, d.str) for d in PERMUTATIONS])
def test_str(p,s):
    assert str(p) == s

@pytest.mark.parametrize('p,s', [(d.p, d.str) for d in PERMUTATIONS])
def test_parse(p,s):
    assert Permutation.parse(s) == p

# vim:set nowrap:
