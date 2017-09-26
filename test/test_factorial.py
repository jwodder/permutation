import pytest
from   permutation import from_factorial_base, to_factorial_base

# <https://oeis.org/A007623>
FACTORIAL = [
    ( 0,       [0]),
    ( 1,       [1]),
    ( 2,     [1,0]),
    ( 3,     [1,1]),
    ( 4,     [2,0]),
    ( 5,     [2,1]),
    ( 6,   [1,0,0]),
    ( 7,   [1,0,1]),
    ( 8,   [1,1,0]),
    ( 9,   [1,1,1]),
    (10,   [1,2,0]),
    (11,   [1,2,1]),
    (12,   [2,0,0]),
    (13,   [2,0,1]),
    (14,   [2,1,0]),
    (15,   [2,1,1]),
    (16,   [2,2,0]),
    (17,   [2,2,1]),
    (18,   [3,0,0]),
    (19,   [3,0,1]),
    (20,   [3,1,0]),
    (21,   [3,1,1]),
    (22,   [3,2,0]),
    (23,   [3,2,1]),
    (24, [1,0,0,0]),
    (25, [1,0,0,1]),
    (26, [1,0,1,0]),
    (27, [1,0,1,1]),
    (28, [1,0,2,0]),
    (29, [1,0,2,1]),
    (30, [1,1,0,0]),
    (31, [1,1,0,1]),
    (32, [1,1,1,0]),
    (33, [1,1,1,1]),
    (34, [1,1,2,0]),
    (35, [1,1,2,1]),
    (36, [1,2,0,0]),
    (37, [1,2,0,1]),
    (38, [1,2,1,0]),
    (39, [1,2,1,1]),
    (40, [1,2,2,0]),
    (41, [1,2,2,1]),
    (42, [1,3,0,0]),
    (43, [1,3,0,1]),
    (44, [1,3,1,0]),
    (45, [1,3,1,1]),
    (46, [1,3,2,0]),
    (47, [1,3,2,1]),
    (48, [2,0,0,0]),
    (49, [2,0,0,1]),
    (50, [2,0,1,0]),
    (463, [3,4,1,0,1]),
]

@pytest.mark.parametrize('n,digits', FACTORIAL)
def test_to_factorial_base(n, digits):
    assert to_factorial_base(n) == digits

def test_bad_to_factorial_base():
    with pytest.raises(ValueError):
        to_factorial_base(-1)

@pytest.mark.parametrize('n,digits', FACTORIAL)
def test_from_factorial_base(n, digits):
    assert from_factorial_base(digits) == n

@pytest.mark.parametrize('digits', [(-1,), (2,), (1,2), (3,0), (4,1,2)])
def test_bad_from_factorial_base(digits):
    with pytest.raises(ValueError):
        from_factorial_base(digits)
