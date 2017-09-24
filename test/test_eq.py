import pytest
from   permutation import Permutation

EQUIV_CLASSES = [
    [
        Permutation(),
        Permutation(1),
        Permutation(1,2),
        Permutation(1,2,3,4,5),
        Permutation.cycle(),
        Permutation.from_cycles(),
        Permutation.from_cycles(()),
    ],

    [
        Permutation(2,1),
        Permutation(2,1,3,4,5),
        Permutation.cycle(1,2),
        Permutation.cycle(2,1),
        Permutation.from_cycles((1,2)),
        Permutation.from_cycles((2,1)),
    ],

    [
        Permutation(2,3,1),
        Permutation(2,3,1,4,5),
        Permutation.cycle(1,2,3),
        Permutation.cycle(2,3,1),
        Permutation.cycle(3,1,2),
        Permutation.from_cycles((1,2,3)),
        Permutation.from_cycles((2,3,1)),
        Permutation.from_cycles((3,1,2)),
    ],

    [
        Permutation(3,1,2),
        Permutation(3,1,2,4,5),
        Permutation.cycle(1,3,2),
        Permutation.cycle(2,1,3),
        Permutation.cycle(3,2,1),
        Permutation.from_cycles((1,3,2)),
        Permutation.from_cycles((2,1,3)),
        Permutation.from_cycles((3,2,1)),
    ],

    [
        Permutation(3,2,1),
        Permutation(3,2,1,4,5),
        Permutation.cycle(1,3),
        Permutation.cycle(3,1),
        Permutation.from_cycles((1,3)),
        Permutation.from_cycles((3,1)),
    ],

    [
        Permutation(2,3,1,5,4),
        Permutation.from_cycles((1,2,3), (4,5)),
        Permutation.from_cycles((1,2,3), (5,4)),
        Permutation.from_cycles((3,1,2), (4,5)),
        Permutation.from_cycles((4,5), (3,1,2)),
        Permutation.from_cycles((4,5), (1,2,3)),
        Permutation.from_cycles((5,4), (1,2,3)),
    ],
]

@pytest.mark.parametrize('p,q',
    [(p,q) for eqcls in EQUIV_CLASSES for p in eqcls for q in eqcls]
)
def test_eq(p,q):
    assert p == q
    assert not (p != q)
    assert hash(p) == hash(q)

@pytest.mark.parametrize('p,q', [
    (p,q) for i, ps in enumerate(EQUIV_CLASSES)
          for qs in EQUIV_CLASSES[:i] + EQUIV_CLASSES[i+1:]
          for p in ps
          for q in qs
])
def test_neq(p,q):
    assert p != q
    assert not (p == q)

@pytest.mark.parametrize('p', [p for eqcls in EQUIV_CLASSES for p in eqcls])
@pytest.mark.parametrize('x', [None, 0, 1, True, False, '(1 2)', (1,2), [1,2]])
def test_neq_other_types(p,x):
    assert p != x
    assert not (p == x)
