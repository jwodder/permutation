""" Permutations of finitely many positive integers """

from   fractions import gcd
from   functools import reduce, total_ordering
import operator

__all__ = ["Permutation"]

@total_ordering
class Permutation(object):
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
        return cls()

    def __call__(self, i):
        return self._map[i-1] if 0 < i <= len(self._map) else i

    def __mul__(self, other):
        return type(self)((self(other(i+1))
                           for i in range(max(self.degree, other.degree))),
                          even = self._even == other._even
                              if self._even is not None
                                  and other._even is not None
                              else None)

    def __repr__(self):
        return '%s(%r)' % (type(self).__name__, self._map)

    def __str__(self):
        cycles = self.to_cycles()
        if cycles:
            return ''.join('(' + ' '.join(map(str,cyc)) + ')' for cyc in cycles)
        else:
            return '1'

    @classmethod
    def parse(cls, s):  # inverse of `__str__`
        s = s.strip()
        if not s:
            raise ValueError('empty argument')
        if s == '1':
            return cls.identity()
        if s[0] != '(':
            raise ValueError('invalid argument')
        cycles = []
        for c in s[1:].split('('):
            c = c.strip()
            if not c or c[-1] != ')':
                raise ValueError('invalid argument')
            cycles.append(int(x) for x in c[:-1].split())
        return cls.from_cycles(cycles)

    def __nonzero__(self):
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
        return len(self._map)

    @property
    def inverse(self):
        newMap = [None] * len(self._map)
        for (a,b) in enumerate(self._map):
            newMap[b-1] = a+1
        return type(self)(newMap, even=self._even, order=self._order)

    @property
    def order(self):
        if self._order is None:
            self._order = reduce(lcm, map(len, self.to_cycles()), 1)
        return self._order

    @property
    def is_even(self):
        if self._even is None:
            self._even = not sum((len(cyc)-1 for cyc in self.to_cycles()),0) % 2
        return self._even

    @property
    def is_odd(self):
        return not self.is_even

    @property
    def sign(self):
        return 1 if self.is_even else -1

    @property
    def lehmer(self):
        if self._lehmer is None:
            left = range(len(self._map), 0, -1)
            self._lehmer = 0
            for x in left[:]:
                i = left.index(self(x))
                del left[i]
                self._lehmer = self._lehmer * x + i
        return self._lehmer

    @classmethod
    def from_lehmer(cls, x):
        if x < 0:
            raise ValueError('argument must be nonnegative')
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
        Returns the permutation representing the transposition of the positive
        integers ``a`` and ``b``
        """
        if a < 1 or b < 1:
            raise ValueError('values must be positive')
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
    def from_cycle(cls, cyc):
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
        return reduce(operator.mul, map(cls.from_cycle, cycles), cls())

    def disjoint(self, other):
        for (i,(a,b)) in enumerate(zip(self._map, other._map)):
            if i+1 != a and i+1 != b:
                return False
        return True

    @classmethod
    def first_of_degree(cls, n):
        """
        Returns the first `Permutation` of degree ``n`` in modified Lehmer code
        order.  If ``n`` is 0 or 1 (or anything less than 0), this is the
        identity.  For higher degrees, this is ``Permutation.transposition(n,
        n-1)``.
        """
        return cls.identity() if n < 2 else cls.transposition(n, n-1)

    def next_permutation(self):
        """ Returns the next `Permutation` in modified Lehmer code order """
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
        Returns the previous `Permutation` in modified Lehmer code order.  If
        ``self`` is the identity (which has Lehmer code 0), a `ValueError` is
        raised.
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
        p = cls()
        while p.degree <= n:
            yield p
            p = p.next_permutation()

    def to_image(self, n=None):
        # Returns the image of 1 through `n` (or self.degree, whichever's
        # bigger) under the permutation
        if n is None or n <= self.degree:
            return self._map
        else:
            return self._map + tuple(range(self.degree+1, n+1))

    @classmethod
    def from_image(cls, img):
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
        if len(xs) < self.degree:
            raise ValueError('sequence must have at least `degree` elements')
        out = [None] * len(xs)
        for i in range(len(xs)):
            out[self(i+1)-1] = xs[i]
        return out


def lcm(x,y):
    d = gcd(x,y)
    return 0 if d == 0 else abs(x*y) // d
