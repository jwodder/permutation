""" Permutations of finitely many positive integers """

from   fractions import gcd
from   functools import reduce, total_ordering
from   itertools import starmap
import operator

__all__ = ["Permutation"]

@total_ordering
class Permutation(object):
    """
    A `Permutation` object represents a permutation of finitely many positive
    integers, i.e., a bijective function from some integer range ``[1,n]`` to
    itself.
    """

    def __init__(self, mapping=(), even=None, order=None, lehmer=None):
        # not for public use
        self._map    = tuple(mapping)
        self._even   = even
        self._order  = order
        self._lehmer = lehmer
        i = len(self._map) - 1
        while i >= 0 and self._map[i] == i+1:
            i -= 1
        self._map = self._map[0:i+1]

    @classmethod
    def identity(cls):
        """
        The identity permutation, i.e., the permutation that returns all inputs
        unchanged
        """
        return cls()

    def __call__(self, i):
        """
        Maps the integer ``i`` through the permutation.  Values less than 1 are
        returned unchanged.

        :type i: int
        :return: the image of ``i`` under the permutation
        """
        return self._map[i-1] if 0 < i <= len(self._map) else i

    def __mul__(self, other):
        """
        Multiplication/composition of permutations.  ``p * q`` returns a
        `Permutation` ``r`` such that ``r(x) == p(q(x))`` for all integers
        ``x``.

        :type other: Permutation
        :rtype: Permutation
        """
        return type(self)((self(other(i+1))
                           for i in range(max(self.degree, other.degree))),
                          even = self._even == other._even
                              if self._even is not None
                                  and other._even is not None
                              else None)

    def __repr__(self):
        return '%s(%r)' % (type(self).__name__, self._map)

    def __str__(self):
        """
        Convert a `Permutation` to cycle notation.  The instance is decomposed
        into cycles with `to_cycles()`, each cycle is written as a
        parenthesized space-separated sequence of integers, and the cycles are
        concatenated.

        When applied to the identity, `__str__` returns ``"1"``.
        """
        cycles = self.to_cycles()
        if cycles:
            return ''.join('(' + ' '.join(map(str,cyc)) + ')' for cyc in cycles)
        else:
            return '1'

    @classmethod
    def parse(cls, s):
        """
        Parse a permutation written in cycle notation.  This is the inverse of
        `__str__`, though it also accepts input with superfluous whitespace.

        :param str s: a permutation written in cycle notation
        :return: the Permutation represented by ``s``
        :rtype: Permutation
        :raises ValueError: if ``s`` is not valid cycle notation for a
            permutation
        """
        s = s.strip()
        if not s:
            raise ValueError(s)
        if s == '1':
            return cls.identity()
        if s[0] != '(':
            raise ValueError(s)
        cycles = []
        for c in s[1:].split('('):
            c = c.strip()
            if not c or c[-1] != ')':
                raise ValueError(s)
            cycles.append(int(x) for x in c[:-1].split())
        return cls.from_cycles(cycles)

    def __nonzero__(self):
        """ A `Permutation` is true iff it is not the identity """
        return self._map != ()

    __bool__ = __nonzero__

    def __eq__(self, other):
        if type(self) is type(other):
            return self._map == other._map
        else:
            return NotImplemented

    def __lt__(self, other):
        # This comparison method produces the same ordering as the modified
        # Lehmer codes.
        if type(self) is type(other):
            return (-other.degree, other._map[::-1]) < \
                (-self.degree, self._map[::-1])
        else:
            return NotImplemented

    def __hash__(self):
        return hash(self._map)

    @property
    def degree(self):
        """
        The degree of the permutation, i.e., the largest integer that it
        permutes (does not map to itself), or 0 if there is no such integer
        (i.e., if the permutation is the identity)
        """
        return len(self._map)

    def inverse(self):
        """
        Returns the inverse of the permutation, i.e., the unique permutation
        that, when multiplied by the invocant on either the left or the right,
        produces the identity

        :rtype: Permutation
        """
        newMap = [None] * len(self._map)
        for (a,b) in enumerate(self._map):
            newMap[b-1] = a+1
        return type(self)(newMap, even=self._even, order=self._order)

    @property
    def order(self):
        """
        The order of the permutation, i.e., the smallest positive integer ``n``
        such that multiplying ``n`` copies of the permutation together produces
        the identity
        """
        if self._order is None:
            self._order = reduce(lcm, map(len, self.to_cycles()), 1)
        return self._order

    @property
    def is_even(self):
        """
        Whether the permutation is even, i.e., can be expressed as the product
        of an even number of transpositions
        """
        if self._even is None:
            self._even = not sum((len(cyc)-1 for cyc in self.to_cycles()),0) % 2
        return self._even

    @property
    def is_odd(self):
        """ Whether the permutation is odd, i.e., not even """
        return not self.is_even

    @property
    def sign(self):
        """
        The sign (a.k.a. signature) of the permutation: 1 if the permutation is
        even, -1 if it is odd
        """
        return 1 if self.is_even else -1

    def modified_lehmer(self):
        """
        Encode the permutation as a nonnegative integer using a modified form
        of `Lehmer codes <https://en.wikipedia.org/wiki/Lehmer_code>`_.  This
        encoding establishes a bijection between permutation values and
        nonnegative integers, with `from_modified_lehmer()` converting values
        in the opposite direction.

        :return: The permutation's modified Lehmer code
        """
        if self._lehmer is None:
            left = range(len(self._map), 0, -1)
            self._lehmer = 0
            for x in left[:]:
                i = left.index(self(x))
                del left[i]
                self._lehmer = self._lehmer * x + i
        return self._lehmer

    @classmethod
    def from_modified_lehmer(cls, x):
        """
        Returns the permutation corresponding to the given modified Lehmer
        code.  This is the inverse of `modified_lehmer()`.

        :param int x: a nonnegative integer
        :return: the `Permutation` with modified Lehmer code ``x``
        :raises ValueError: if ``x`` is less than 0
        """
        if x < 0:
            raise ValueError(x)
        x0 = x
        mapping = []
        f = 1
        while x > 0:
            c = x % f
            for (i,y) in enumerate(mapping):
                if y >= c:
                    mapping[i] += 1
            mapping.append(c)
            x //= f
            f += 1
        return cls((len(mapping)-c for c in mapping), lehmer=x0)

    def to_cycles(self):
        """
        Decompose the permutation into a product of disjoint cycles.
        `to_cycles()` returns a list of cycles in which each cycle is a tuple
        of integers.  Each cycle ``c`` is a sub-permutation that maps ``c[0]``
        to ``c[1]``, ``c[1]`` to ``c[2]``, etc., finally mapping ``c[-1]`` back
        around to ``c[0]``.  The permutation is then the product of these
        cycles.

        Each cycle is at least 2 elements in size and places its smallest
        element at index 0.  Cycles are ordered by their index 0's in
        increasing order.  No two cycles share an element.

        When the permutation is the identity, `to_cycles()` returns an empty
        list.

        :return: the cycle decomposition of the permutation
        """
        cmap = list(self._map)
        cycles = []
        for i in range(len(cmap)):
            if cmap[i] != 0 and cmap[i] != i+1:
                x = i+1
                cyke = [x]
                y = cmap[x-1]
                cmap[x-1] = 0
                while y != x:
                    cyke.append(y)
                    nxt = cmap[y-1]
                    cmap[y-1] = 0
                    y = nxt
                cycles.append(tuple(cyke))
        return cycles

    @classmethod
    def transposition(cls, a, b):
        """
        Returns the transposition of ``a`` and ``b``, i.e., the permutation
        that maps ``a`` to ``b``, maps ``b`` to ``a``, and leaves all other
        values unchanged.  When ``a`` equals ``b``, `transposition` returns
        `identity`.

        :param int a: a positive integer
        :param int b: a positive integer
        :return: the transposition of ``a`` and ``b``
        :rtype: Permutation
        :raises ValueError: if ``a`` or ``b`` is less than 1
        """
        if a < 1:
            raise ValueError(a)
        elif b < 1:
            raise ValueError(b)
        elif a == b:
            return cls()
        else:
            # For $a<b$, $Lehmer((a b)) = (b-a) (b-1)! + \sum_{i=a}^{b-2} i!$
            big = max(a,b)
            small = min(a,b)
            lehmer = 0
            fac = reduce(operator.mul, range(1, small+1))
            for i in range(small, big-1):
                lehmer += fac
                fac *= i+1
            lehmer += fac * (big-small)
            return cls((b if x == a else a if x == b else x
                        for x in range(1, big+1)),
                       even=False, order=2, lehmer=lehmer)

    @classmethod
    def cycle(cls, *cyc):
        """
        Construct a `cyclic permutation
        <https://en.wikipedia.org/wiki/Cyclic_permutation>`_ from a sequence of
        unique positive integers.  If ``p = Permutation.cycle(*cyc)``, then
        ``p(cyc[0]) == cyc[1]``, p(cyc[1]) == cyc[2]``, etc., and ``p(cyc[-1])
        == cyc[0]``, with all other values returned unchanged.

        When ``cyc`` is empty, `cycle` returns `identity`.

        :param cyc: zero or more unique positive integers
        :return: the permutation represented by the given cycle
        :raises ValueError:
            - if ``cyc`` contains a value less than 1
            - if ``cyc`` contains the same value more than once
        """
        cyc = list(cyc)
        if len(cyc) < 2:
            return cls()
        mapping = {}
        maxVal = 0
        for (i,v) in enumerate(cyc):
            if v < 1:
                raise ValueError('values must be positive')
            if v in mapping:
                raise ValueError('%s appears more than once in cycle' % (v,))
            mapping[v] = cyc[i+1] if i < len(cyc)-1 else cyc[0]
            if v > maxVal:
                maxVal = v
        return cls((mapping.get(i,i) for i in range(1, maxVal+1)),
                   even = len(cyc) % 2, order=len(cyc))

    @classmethod
    def from_cycles(cls, cycles):
        """
        Construct the product of zero or more cyclic permutations.  Each
        element of the iterable ``cycles`` is converted to a `Permutation` with
        `cycle`, and the results are then multiplied together and returned.

        The cycles in ``cycles`` need not be disjoint.  When ``cycles`` is
        empty, `from_cycles` returns `identity`.

        This is the inverse of `to_cycles`.

        :param iterable cycles:
        :return: the `Permutation` represented by the product of the cycles
        :raises ValueError:
            - if any cycle contains a value less than 1
            - if any cycle contains the same value more than once
        """
        return reduce(operator.mul, starmap(cls.cycle, cycles), cls())

    def disjoint(self, other):
        """
        Returns `True` iff the permutation and ``other`` are disjoint, i.e.,
        iff they do not permute any of the same integers

        :param Permutation other: a Permutation to compare against
        :rtype: bool
        """
        for (i,(a,b)) in enumerate(zip(self._map, other._map)):
            if i+1 != a and i+1 != b:
                return False
        return True

    @classmethod
    def first_of_degree(cls, n):
        """
        Returns the first permutation (in modified Lehmer code order) of degree
        ``n``.  If ``n`` is 0 or 1 (or anything less than 0), this is
        `identity`.  For higher degrees, this is ``Permutation.transposition(n,
        n-1)``.

        :type n: int
        :rtype: Permutation
        """
        return cls.identity() if n < 2 else cls.transposition(n, n-1)

    def next_permutation(self):
        """
        Returns the next `Permutation` in modified Lehmer code order (also the
        least `Permutation` greater than the invocant)
        """
        if self.degree < 2:
            return self.transposition(1,2)
        else:
            lehmer2 = self._lehmer+1 if self._lehmer is not None else None
            map2 = list(self._map)
            for i in range(1, len(map2)):
                if map2[i] > map2[i-1]:
                    i2 = 0
                    while map2[i] <= map2[i2]:
                        i2 += 1
                    map2[i], map2[i2] = map2[i2], map2[i]
                    map2[:i] = reversed(map2[:i])
                    return type(self)(map2, lehmer=lehmer2)
            return self.first_of_degree(self.degree+1)

    def prev_permutation(self):
        """
        Returns the previous `Permutation` in modified Lehmer code order (also
        the greatest `Permutation` less than the invocant)

        :raises ValueError: if called on the identity `Permutation` (which has
            modified Lehmer code 0)
        """
        if self.degree < 2:
            raise ValueError('cannot decrement identity')
        lehmer2 = self._lehmer-1 if self._lehmer is not None else None
        map2 = list(self._map)
        for i in range(1, len(map2)):
            if map2[i] < map2[i-1]:
                i2 = 0
                while map2[i] >= map2[i2]:
                    i2 += 1
                map2[i], map2[i2] = map2[i2], map2[i]
                map2[:i] = reversed(map2[:i])
                return type(self)(map2, lehmer=lehmer2)

    @classmethod
    def s_n(cls, n):
        """
        Generates all permutations in the symmetric group of degree ``n``,
        i.e., all permutations with degree less than or equal to ``n``, i.e.,
        all permutations from `identity` up to but not including
        ``first_of_degree(n+1)``.  The permutations are yielded in ascending
        order of their modified Lehmer codes.

        :param int n: a nonnegative integer
        :return: a generator of all `Permutation`s with degree ``n`` or less
        :raises ValueError: if ``n`` is less than 0
        """
        if n < 0:
            raise ValueError(n)
        p = cls()
        while p.degree <= n:
            yield p
            p = p.next_permutation()

    def to_image(self, n=None):
        """
        Return a tuple of the results of applying the permutation to the
        integers 1 through ``n``, or through `degree` if ``n`` is unspecified
        or less than `degree`.  If ``v = p.to_image()`, then ``v[0] == p(1)``,
        ``v[1] == p(2)``, etc.

        When the permutation is the identity, `to_image` called without an
        argument returns an empty tuple.

        :param int n: the minimum length of the image to return
        :return: the image of 1 through either ``n`` or `degree` (whichever is
            larger) under the permutation
        """
        if n is None or n <= self.degree:
            return self._map
        else:
            return self._map + tuple(range(self.degree+1, n+1))

    @classmethod
    def from_image(cls, img):
        """
        Construct a permutation from a sequence of integers that specifies the
        results of applying the target permutation to the integers 1 through
        some ``n``.  If ``p = Permutation.from_image(img)``, then ``p(1) ==
        img[0]``, ``p(2) == img[1]``, etc.

        When ``img`` is empty, `from_image` returns `identity`.

        :param sequence img: the image of the permutation to construct
        :return: the `Permutation` with image ``img``
        :raises ValueError:
            - if ``img`` contains a value less than 1
            - if ``img`` contains the same value more than once
            - if ``img`` does not contain every integer value from 1 through
              ``len(img)``
        """
        img = tuple(img)
        used = [False] * len(img)
        for i in img:
            if i < 1:
                raise ValueError('values must be positive')
            if i > len(img):
                raise ValueError('value missing from input')
            if used[i-1]:
                raise ValueError('value repeated in input')
            used[i-1] = True
        return cls(img)

    def permute_seq(self, xs):
        """
        Reorders the elements of a sequence according to the permutation

        :param xs: a sequence of at least `degree` elements
        :return: a permuted sequence
        :raise ValueError: if ``len(xs)`` is less than `degree`
        """
        if len(xs) < self.degree:
            raise ValueError('sequence must have at least `degree` elements')
        out = [None] * len(xs)
        for i in range(len(xs)):
            out[self(i+1)-1] = xs[i]
        return out


def lcm(x,y):
    d = gcd(x,y)
    return 0 if d == 0 else abs(x*y) // d
