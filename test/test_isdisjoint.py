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

DISJOINT = [[True] * 24] + [[True] + [False] * 23 for _ in range(23)]
DISJOINT[1][6]  = DISJOINT[6][1]  = True  # (1 2), (3 4)
DISJOINT[2][21] = DISJOINT[21][2] = True  # (2 3), (1 4)
DISJOINT[5][14] = DISJOINT[14][5] = True  # (1 3), (2 4)

@pytest.mark.parametrize('p,q,d', [
    (p, q, DISJOINT[i][j]) for i,p in enumerate(S4) for j,q in enumerate(S4)
])
def test_is_disjoint(p, q, d):
    assert p.isdisjoint(q) is d
