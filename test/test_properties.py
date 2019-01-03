from   collections import namedtuple
import pytest
from   permutation import Permutation

PermData = namedtuple(
    'PermData',
    'p degree order even sign bool mod_lehmer inversions cycles str image image6 permuted',
)

PERMUTATIONS = [
    PermData(Permutation(),            0, 1, True,   1, False,   0,     0, [],                  '1',               (),            (1,2,3,4,5,6), ()),
    PermData(Permutation(2,1),         2, 2, False, -1, True,    1,     1, [(1,2)],             '(1 2)',           (2,1),         (2,1,3,4,5,6), (2,1)),
    PermData(Permutation(1,3,2),       3, 2, False, -1, True,    2,     1, [(2,3)],             '(2 3)',           (1,3,2),       (1,3,2,4,5,6), (1,3,2)),
    PermData(Permutation(3,1,2),       3, 3, True,   1, True,    3,     2, [(1,3,2)],           '(1 3 2)',         (3,1,2),       (3,1,2,4,5,6), (2,3,1)),
    PermData(Permutation(2,3,1),       3, 3, True,   1, True,    4,     2, [(1,2,3)],           '(1 2 3)',         (2,3,1),       (2,3,1,4,5,6), (3,1,2)),
    PermData(Permutation(3,2,1),       3, 2, False, -1, True,    5,     3, [(1,3)],             '(1 3)',           (3,2,1),       (3,2,1,4,5,6), (3,2,1)),
    PermData(Permutation(1,2,4,3),     4, 2, False, -1, True,    6,     1, [(3,4)],             '(3 4)',           (1,2,4,3),     (1,2,4,3,5,6), (1,2,4,3)),
    PermData(Permutation(2,1,4,3),     4, 2, True,   1, True,    7,     2, [(1,2),(3,4)],       '(1 2)(3 4)',      (2,1,4,3),     (2,1,4,3,5,6), (2,1,4,3)),
    PermData(Permutation(2,3,4,1),     4, 4, False, -1, True,   18,     3, [(1,2,3,4)],         '(1 2 3 4)',       (2,3,4,1),     (2,3,4,1,5,6), (4,1,2,3)),
    PermData(Permutation(2,3,1,5,4),   5, 6, False, -1, True,   28,     3, [(1,2,3),(4,5)],     '(1 2 3)(4 5)',    (2,3,1,5,4),   (2,3,1,5,4,6), (3,1,2,5,4)),
    PermData(Permutation(2,3,4,5,1),   5, 5, True,   1, True,   96,     4, [(1,2,3,4,5)],       '(1 2 3 4 5)',     (2,3,4,5,1),   (2,3,4,5,1,6), (5,1,2,3,4)),
    PermData(Permutation(5,4,3,2,1),   5, 2, True,   1, True,  119,    10, [(1,5),(2,4)],       '(1 5)(2 4)',      (5,4,3,2,1),   (5,4,3,2,1,6), (5,4,3,2,1)),
    PermData(Permutation(2,1,4,3,6,5), 6, 2, False, -1, True,  127,     3, [(1,2),(3,4),(5,6)], '(1 2)(3 4)(5 6)', (2,1,4,3,6,5), (2,1,4,3,6,5), (2,1,4,3,6,5)),
    PermData(Permutation(2,3,4,1,6,5), 6, 4, True,   1, True,  138,     4, [(1,2,3,4),(5,6)],   '(1 2 3 4)(5 6)',  (2,3,4,1,6,5), (2,3,4,1,6,5), (4,1,2,3,6,5)),
    PermData(Permutation(2,3,1,5,6,4), 6, 3, True,   1, True,  244,     4, [(1,2,3),(4,5,6)],   '(1 2 3)(4 5 6)',  (2,3,1,5,6,4), (2,3,1,5,6,4), (3,1,2,6,4,5)),
    PermData(Permutation(2,3,4,5,6,1), 6, 6, False, -1, True,  600,     5, [(1,2,3,4,5,6)],     '(1 2 3 4 5 6)',   (2,3,4,5,6,1), (2,3,4,5,6,1), (6,1,2,3,4,5)),
]

@pytest.mark.parametrize('p,degree', [(pd.p, pd.degree) for pd in PERMUTATIONS])
def test_degree(p, degree):
    assert p.degree == degree

@pytest.mark.parametrize('p,order', [(pd.p, pd.order) for pd in PERMUTATIONS])
def test_order(p, order):
    assert p.order == order

@pytest.mark.parametrize('p,even', [(pd.p, pd.even) for pd in PERMUTATIONS])
def test_is_even(p, even):
    assert p.is_even is even

@pytest.mark.parametrize('p,even', [(pd.p, pd.even) for pd in PERMUTATIONS])
def test_is_odd(p, even):
    assert p.is_odd is (not even)

@pytest.mark.parametrize('p,sign', [(pd.p, pd.sign) for pd in PERMUTATIONS])
def test_sign(p, sign):
    assert p.sign == sign

@pytest.mark.parametrize('p,code', [(d.p, d.mod_lehmer) for d in PERMUTATIONS])
def test_left_lehmer(p, code):
    assert p.left_lehmer() == code

@pytest.mark.parametrize('p,code', [(d.p, d.mod_lehmer) for d in PERMUTATIONS])
def test_from_left_lehmer(p, code):
    assert Permutation.from_left_lehmer(code) == p

def test_bad_from_left_lehmer():
    with pytest.raises(ValueError):
        Permutation.from_left_lehmer(-1)

@pytest.mark.parametrize('p,cycles', [(d.p, d.cycles) for d in PERMUTATIONS])
def test_to_cycles(p, cycles):
    assert p.to_cycles() == cycles

@pytest.mark.parametrize('p,cycles', [(d.p, d.cycles) for d in PERMUTATIONS])
def test_from_cycles(p, cycles):
    assert Permutation.from_cycles(*cycles) == p

@pytest.mark.parametrize('p,s', [(d.p, d.str) for d in PERMUTATIONS])
def test_str(p,s):
    assert str(p) == s

@pytest.mark.parametrize('p,s', [(d.p, d.str) for d in PERMUTATIONS])
def test_parse(p,s):
    assert Permutation.parse(s) == p

@pytest.mark.parametrize('p,image', [(d.p, d.image) for d in PERMUTATIONS])
def test_repr(p, image):
    assert repr(p) == 'permutation.Permutation' + repr(image)

@pytest.mark.parametrize('p,b', [(d.p, d.bool) for d in PERMUTATIONS])
def test_bool(p,b):
    assert bool(p) is b

@pytest.mark.parametrize('p,image', [(d.p, d.image) for d in PERMUTATIONS])
def test_to_image(p, image):
    assert p.to_image() == image

@pytest.mark.parametrize('p,image6', [(d.p, d.image6) for d in PERMUTATIONS])
def test_to_extra_image(p, image6):
    assert p.to_image(6) == image6

@pytest.mark.parametrize('p,degree', [(d.p, d.degree) for d in PERMUTATIONS])
def test_bad_to_image(p, degree):
    with pytest.raises(ValueError):
        p.to_image(degree - 1)

@pytest.mark.parametrize('p,image', [(d.p, d.image) for d in PERMUTATIONS])
def test_from_image(p, image):
    assert Permutation(*image) == p

@pytest.mark.parametrize('p,permuted', [(d.p, d.permuted) for d in PERMUTATIONS])
def test_permute(p, permuted):
    assert p.permute(range(1, p.degree+1)) == permuted

@pytest.mark.parametrize('p,degree', [(d.p, d.degree) for d in PERMUTATIONS if d.degree > 0])
def test_bad_permute(p, degree):
    with pytest.raises(ValueError):
        p.permute(range(1, p.degree))

@pytest.mark.parametrize('p,inversions', [(d.p, d.inversions) for d in PERMUTATIONS])
def test_inversions(p, inversions):
    assert p.inversions() == inversions

# vim:set nowrap:
