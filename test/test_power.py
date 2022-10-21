import pytest
from permutation import Permutation


BASES = [
    Permutation(),
    Permutation.from_cycles((1, 2)),
    Permutation.from_cycles((2, 3)),
    Permutation.from_cycles((1, 3, 2)),
    Permutation.from_cycles((1, 2, 4)),
    Permutation.from_cycles((1, 3, 2, 4)),
    Permutation.from_cycles((1, 4), (2, 3)),
]

EXPONENTS = range(-2, 3)

POWERS = [
    [Permutation()] * 5,
    [
        Permutation(),
        Permutation.from_cycles((2, 1)),
        Permutation(),
        Permutation.from_cycles((1, 2)),
        Permutation()
    ],
    [
        Permutation(),
        Permutation.from_cycles((3, 2)),
        Permutation(),
        Permutation.from_cycles((2, 3)),
        Permutation()
    ],
    [
        Permutation.from_cycles((1, 3, 2)),
        Permutation.from_cycles((1, 2, 3)),
        Permutation(),
        Permutation.from_cycles((1, 3, 2)),
        Permutation.from_cycles((1, 2, 3))
    ],
    [
        Permutation.from_cycles((1, 2, 4)),
        Permutation.from_cycles((1, 4, 2)),
        Permutation(),
        Permutation.from_cycles((1, 2, 4)),
        Permutation.from_cycles((1, 4, 2))
    ],
    [
        Permutation.from_cycles((1, 2), (3, 4)),
        Permutation.from_cycles((1, 4, 2, 3)),
        Permutation(),
        Permutation.from_cycles((1, 3, 2, 4)),
        Permutation.from_cycles((1, 2), (3, 4))
    ],
    [
        Permutation(),
        Permutation.from_cycles((1, 4), (2, 3)),
        Permutation(),
        Permutation.from_cycles((1, 4), (2, 3)),
        Permutation()
    ]
]


@pytest.mark.parametrize("base", range(len(BASES)))
@pytest.mark.parametrize("exponent", range(len(EXPONENTS)))
def test_power(base: int, exponent: int) -> None:
    assert BASES[base] ** EXPONENTS[exponent] == POWERS[base][exponent]
