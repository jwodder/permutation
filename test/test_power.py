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
        Permutation(),
    ],
    [
        Permutation(),
        Permutation.from_cycles((3, 2)),
        Permutation(),
        Permutation.from_cycles((2, 3)),
        Permutation(),
    ],
    [
        Permutation.from_cycles((1, 3, 2)),
        Permutation.from_cycles((1, 2, 3)),
        Permutation(),
        Permutation.from_cycles((1, 3, 2)),
        Permutation.from_cycles((1, 2, 3)),
    ],
    [
        Permutation.from_cycles((1, 2, 4)),
        Permutation.from_cycles((1, 4, 2)),
        Permutation(),
        Permutation.from_cycles((1, 2, 4)),
        Permutation.from_cycles((1, 4, 2)),
    ],
    [
        Permutation.from_cycles((1, 2), (3, 4)),
        Permutation.from_cycles((1, 4, 2, 3)),
        Permutation(),
        Permutation.from_cycles((1, 3, 2, 4)),
        Permutation.from_cycles((1, 2), (3, 4)),
    ],
    [
        Permutation(),
        Permutation.from_cycles((1, 4), (2, 3)),
        Permutation(),
        Permutation.from_cycles((1, 4), (2, 3)),
        Permutation(),
    ],
]


@pytest.mark.parametrize("base", range(len(BASES)))
@pytest.mark.parametrize("exponent", range(len(EXPONENTS)))
def test_power(base: int, exponent: int) -> None:
    assert BASES[base] ** EXPONENTS[exponent] == POWERS[base][exponent]


@pytest.mark.parametrize(
    "exponent,power",
    [
        (-127, Permutation.from_cycles((1, 2), (3, 5, 4))),
        (-12, Permutation()),
        (-6, Permutation()),
        (-5, Permutation.from_cycles((1, 2), (3, 4, 5))),
        (-4, Permutation.cycle(3, 5, 4)),
        (-3, Permutation.cycle(1, 2)),
        (-2, Permutation.cycle(3, 4, 5)),
        (-1, Permutation.from_cycles((1, 2), (3, 5, 4))),
        (0, Permutation()),
        (1, Permutation.from_cycles((1, 2), (3, 4, 5))),
        (2, Permutation.cycle(3, 5, 4)),
        (3, Permutation.cycle(1, 2)),
        (4, Permutation.cycle(3, 4, 5)),
        (5, Permutation.from_cycles((1, 2), (3, 5, 4))),
        (6, Permutation()),
        (12, Permutation()),
        (127, Permutation.from_cycles((1, 2), (3, 4, 5))),
    ],
)
def test_more_powers(exponent: int, power: Permutation) -> None:
    p = Permutation.from_cycles((1, 2), (3, 4, 5))
    assert p**exponent == power
