import pytest
from   permutation import Permutation

@pytest.mark.parametrize('p,q', [
    (Permutation(),                              Permutation()),
    (Permutation.cycle(1,2),                     Permutation.cycle(1,2)),
    (Permutation.cycle(2,1),                     Permutation.cycle(1,2)),
    (Permutation.cycle(2,3),                     Permutation.cycle(2,3)),
    (Permutation.cycle(1,3,2),                   Permutation.cycle(1,2,3)),
    (Permutation.cycle(1,3),                     Permutation.cycle(1,3)),
    (Permutation.cycle(3,4),                     Permutation.cycle(3,4)),
    (Permutation.from_cycles((1,2),(3,4)),       Permutation.from_cycles((1,2),(3,4))),
    (Permutation.cycle(1,2,3,4),                 Permutation.cycle(4,3,2,1)),
    (Permutation.from_cycles((1,2,3),(4,5)),     Permutation.from_cycles((3,2,1),(4,5))),
    (Permutation.cycle(1,2,3,4,5),               Permutation.cycle(5,4,3,2,1)),
    (Permutation.from_cycles((1,5),(2,4)),       Permutation.from_cycles((1,5),(2,4))),
    (Permutation.from_cycles((1,2),(3,4),(5,6)), Permutation.from_cycles((1,2),(3,4),(5,6))),
    (Permutation.from_cycles((1,2,3,4),(5,6)),   Permutation.from_cycles((4,3,2,1),(5,6))),
    (Permutation.from_cycles((1,2,3),(4,5,6)),   Permutation.from_cycles((3,2,1),(6,5,4))),
    (Permutation.cycle(1,2,3,4,5,6),             Permutation.cycle(6,5,4,3,2,1)),
])
def test_inverse(p,q):
    assert p.inverse() == q
    assert q.inverse() == p
    assert p*q == q*p == Permutation()

# vim:set nowrap:
