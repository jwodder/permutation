from six.moves   import zip_longest
from permutation import Permutation

S4 = [
    Permutation.identity(),
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
    for i,(p,q) in enumerate(zip_longest(Permutation.s_n(4), S4)):
        assert p == q
        assert p.modified_lehmer() == i
