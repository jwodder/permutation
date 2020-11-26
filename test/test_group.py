from   itertools   import zip_longest
import pytest
from   permutation import Permutation

S4 = [
    Permutation(),
    Permutation.from_cycles((1,2)),
    Permutation.from_cycles((2,3)),
    Permutation.from_cycles((1,3,2)),
    Permutation.from_cycles((1,2,3)),
    Permutation.from_cycles((1,3)),
    Permutation.from_cycles((3,4)),
    Permutation.from_cycles((1,2),(3,4)),
    Permutation.from_cycles((2,4,3)),
    Permutation.from_cycles((1,4,3,2)),
    Permutation.from_cycles((1,2,4,3)),
    Permutation.from_cycles((1,4,3)),
    Permutation.from_cycles((2,3,4)),
    Permutation.from_cycles((1,3,4,2)),
    Permutation.from_cycles((2,4)),
    Permutation.from_cycles((1,4,2)),
    Permutation.from_cycles((1,3),(2,4)),
    Permutation.from_cycles((1,4,2,3)),
    Permutation.from_cycles((1,2,3,4)),
    Permutation.from_cycles((1,3,4)),
    Permutation.from_cycles((1,2,4)),
    Permutation.from_cycles((1,4)),
    Permutation.from_cycles((1,3,2,4)),
    Permutation.from_cycles((1,4),(2,3)),
]

def test_s4():
    for i,(p,q) in enumerate(zip_longest(Permutation.group(4), S4)):
        assert p == q
        assert p.left_lehmer() == i

def test_next_permutation():
    for i in range(len(S4)-1):
        assert S4[i].next_permutation() == S4[i+1]
        assert S4[i].left_lehmer()+1 == S4[i+1].left_lehmer()

def test_prev_permutation():
    for i in range(len(S4)-1):
        assert S4[i+1].prev_permutation() == S4[i]
        assert S4[i+1].left_lehmer()-1 == S4[i].left_lehmer()

def test_prev_permutation_identity():
    with pytest.raises(ValueError):
        Permutation().prev_permutation()

def test_s0():
    assert list(Permutation.group(0)) == [Permutation()]
    assert list(Permutation.group(1)) == [Permutation()]

def test_bad_group():
    with pytest.raises(ValueError):
        Permutation.group(-1)
