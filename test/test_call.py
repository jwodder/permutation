from __future__ import annotations
import pytest
from permutation import Permutation


@pytest.mark.parametrize(
    "img",
    [
        (1, 2, 3, 4, 5, 6),
        (2, 1, 3, 4, 5, 6),
        (1, 3, 2, 4, 5, 6),
        (3, 1, 2, 4, 5, 6),
        (2, 3, 1, 4, 5, 6),
        (3, 2, 1, 4, 5, 6),
        (1, 2, 4, 3, 5, 6),
        (2, 1, 4, 3, 5, 6),
        (1, 4, 2, 3, 5, 6),
        (4, 1, 2, 3, 5, 6),
        (2, 4, 1, 3, 5, 6),
        (4, 2, 1, 3, 5, 6),
        (1, 3, 4, 2, 5, 6),
        (3, 1, 4, 2, 5, 6),
        (1, 4, 3, 2, 5, 6),
        (4, 1, 3, 2, 5, 6),
        (3, 4, 1, 2, 5, 6),
        (4, 3, 1, 2, 5, 6),
        (2, 3, 4, 1, 5, 6),
        (3, 2, 4, 1, 5, 6),
        (2, 4, 3, 1, 5, 6),
        (4, 2, 3, 1, 5, 6),
        (3, 4, 2, 1, 5, 6),
        (4, 3, 2, 1, 5, 6),
    ],
)
def test_call(img: tuple[int, ...]) -> None:
    p = Permutation(*img)
    for x, y in enumerate(img, start=1):
        assert p(x) == y
    for x in (0, -1, 10, -10):
        assert p(x) == x
