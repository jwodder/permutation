import pytest
from   permutation import Permutation

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

CAYLEY = [
    [ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
    [ 1,  0,  4,  5,  2,  3,  7,  6, 10, 11,  8,  9, 18, 19, 20, 21, 22, 23, 12, 13, 14, 15, 16, 17],
    [ 2,  3,  0,  1,  5,  4, 12, 13, 14, 15, 16, 17,  6,  7,  8,  9, 10, 11, 19, 18, 22, 23, 20, 21],
    [ 3,  2,  5,  4,  0,  1, 13, 12, 16, 17, 14, 15, 19, 18, 22, 23, 20, 21,  6,  7,  8,  9, 10, 11],
    [ 4,  5,  1,  0,  3,  2, 18, 19, 20, 21, 22, 23,  7,  6, 10, 11,  8,  9, 13, 12, 16, 17, 14, 15],
    [ 5,  4,  3,  2,  1,  0, 19, 18, 22, 23, 20, 21, 13, 12, 16, 17, 14, 15,  7,  6, 10, 11,  8,  9],
    [ 6,  7,  8,  9, 10, 11,  0,  1,  2,  3,  4,  5, 14, 15, 12, 13, 17, 16, 20, 21, 18, 19, 23, 22],
    [ 7,  6, 10, 11,  8,  9,  1,  0,  4,  5,  2,  3, 20, 21, 18, 19, 23, 22, 14, 15, 12, 13, 17, 16],
    [ 8,  9,  6,  7, 11, 10, 14, 15, 12, 13, 17, 16,  0,  1,  2,  3,  4,  5, 21, 20, 23, 22, 18, 19],
    [ 9,  8, 11, 10,  6,  7, 15, 14, 17, 16, 12, 13, 21, 20, 23, 22, 18, 19,  0,  1,  2,  3,  4,  5],
    [10, 11,  7,  6,  9,  8, 20, 21, 18, 19, 23, 22,  1,  0,  4,  5,  2,  3, 15, 14, 17, 16, 12, 13],
    [11, 10,  9,  8,  7,  6, 21, 20, 23, 22, 18, 19, 15, 14, 17, 16, 12, 13,  1,  0,  4,  5,  2,  3],
    [12, 13, 14, 15, 16, 17,  2,  3,  0,  1,  5,  4,  8,  9,  6,  7, 11, 10, 22, 23, 19, 18, 21, 20],
    [13, 12, 16, 17, 14, 15,  3,  2,  5,  4,  0,  1, 22, 23, 19, 18, 21, 20,  8,  9,  6,  7, 11, 10],
    [14, 15, 12, 13, 17, 16,  8,  9,  6,  7, 11, 10,  2,  3,  0,  1,  5,  4, 23, 22, 21, 20, 19, 18],
    [15, 14, 17, 16, 12, 13,  9,  8, 11, 10,  6,  7, 23, 22, 21, 20, 19, 18,  2,  3,  0,  1,  5,  4],
    [16, 17, 13, 12, 15, 14, 22, 23, 19, 18, 21, 20,  3,  2,  5,  4,  0,  1,  9,  8, 11, 10,  6,  7],
    [17, 16, 15, 14, 13, 12, 23, 22, 21, 20, 19, 18,  9,  8, 11, 10,  6,  7,  3,  2,  5,  4,  0,  1],
    [18, 19, 20, 21, 22, 23,  4,  5,  1,  0,  3,  2, 10, 11,  7,  6,  9,  8, 16, 17, 13, 12, 15, 14],
    [19, 18, 22, 23, 20, 21,  5,  4,  3,  2,  1,  0, 16, 17, 13, 12, 15, 14, 10, 11,  7,  6,  9,  8],
    [20, 21, 18, 19, 23, 22, 10, 11,  7,  6,  9,  8,  4,  5,  1,  0,  3,  2, 17, 16, 15, 14, 13, 12],
    [21, 20, 23, 22, 18, 19, 11, 10,  9,  8,  7,  6, 17, 16, 15, 14, 13, 12,  4,  5,  1,  0,  3,  2],
    [22, 23, 19, 18, 21, 20, 16, 17, 13, 12, 15, 14,  5,  4,  3,  2,  1,  0, 11, 10,  9,  8,  7,  6],
    [23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10,  9,  8,  7,  6,  5,  4,  3,  2,  1,  0],
]

@pytest.mark.parametrize('i', range(24))
@pytest.mark.parametrize('j', range(24))
def test_mul(i,j):
    assert S4[i] * S4[j] == S4[CAYLEY[i][j]]

# vim:set nowrap: