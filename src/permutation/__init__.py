"""
Permutations of finitely many positive integers

``permutation`` provides a ``Permutation`` class for representing `permutations
<https://en.wikipedia.org/wiki/Permutation>`_ of finitely many positive
integers in Python.  Supported operations & properties include inverses, (group
theoretic) order, parity, composition/multiplication, cycle decomposition,
cycle notation, word representation, Lehmer codes, and, of course, use as a
callable on integers.

Visit <https://github.com/jwodder/permutation> or <http://permutation.rtfd.io>
for more information.
"""

from __future__ import annotations
from collections.abc import Iterable, Iterator, Sequence
from functools import reduce
from itertools import starmap
from math import gcd
import operator
import re
from typing import Any, List, Optional, TypeVar, cast

__version__ = "0.5.0.dev1"
__author__ = "John Thorvald Wodder II"
__author_email__ = "permutation@varonathe.org"
__license__ = "MIT"
__url__ = "https://github.com/jwodder/permutation"

__all__ = ["Permutation"]

T = TypeVar("T")


class Permutation:
    """
    A `Permutation` object represents a `permutation
    <https://en.wikipedia.org/wiki/Permutation>`_ of finitely many positive
    integers, i.e., a bijective function from some integer range :math:`[1,n]`
    to itself.

    `Permutation`\\s are hashable and immutable.  They can be compared for
    equality but not for ordering/sorting.
    """

    def __init__(self, *img: int) -> None:
        """
        Construct a permutation from a word representation.  The arguments are
        the images of the integers 1 through some :math:`n` under the
        permutation to construct.

        For example, ``Permutation(5, 4, 3, 6, 1, 2)`` is the permutation that
        maps 1 to 5, 2 to 4, 3 to itself, 4 to 6, 5 to 1, and 6 to 2.
        ``Permutation()`` (with no arguments) evaluates to the identity
        permutation (i.e., the permutation that returns all inputs unchanged).

        :meta autosection: construction
        """
        d = len(img)
        used = [False] * d
        for i in img:
            if i < 1:
                raise ValueError("values must be positive")
            if i > d:
                raise ValueError("value missing from input")
            if used[i - 1]:
                raise ValueError("value repeated in input")
            used[i - 1] = True
        while d > 0 and img[d - 1] == d:
            d -= 1
        self.__map: tuple[int, ...] = img[:d]

    def __call__(self, i: int) -> int:
        """
        Map an integer through the permutation.  Values less than 1 are
        returned unchanged.

        :param int i:
        :return: the image of ``i`` under the permutation
        :meta autosection: operations
        """
        return self.__map[i - 1] if 0 < i <= len(self.__map) else i

    def __mul__(self, other: Permutation) -> Permutation:
        """
        Multiplication/composition of permutations.  ``p * q`` returns a
        `Permutation` ``r`` such that ``r(x) == p(q(x))`` for all integers
        ``x``.

        :param Permutation other:
        :rtype: Permutation
        :meta autosection: operations
        """
        return type(self)(
            *(self(other(i + 1)) for i in range(max(self.degree, other.degree)))
        )

    def __pow__(self, n: int) -> Permutation:
        """
        Power/repeated composition of permutations.

        - ``p ** 0 == Permutation()``
        - ``p ** n == p ** (n - 1) * p``
        - ``p ** -n == p.inverse() ** n``

        :param int n: exponent
        :rtype: Permutation
        :meta autosection: operations
        """
        if n == 0:
            return type(self)()
        elif n < 0:
            n *= -1
            p = self.inverse()
        else:
            p = self
        while not (n & 1):
            p *= p
            n >>= 1
        agg = p
        p *= p
        n >>= 1
        while n > 0:
            if n & 1:
                agg *= p
            p *= p
            n >>= 1
        return agg

    def __repr__(self) -> str:
        return "{0.__module__}.{0.__name__}{1!r}".format(type(self), self.__map)

    def __str__(self) -> str:
        """
        Convert a `Permutation` to `cycle notation`_.  The instance is
        decomposed into cycles with `to_cycles()`, each cycle is written as a
        parenthesized space-separated sequence of integers, and the cycles are
        concatenated.

        ``str(Permutation())`` is ``"1"``.

        This is the inverse of `parse`.

        .. _cycle notation:
           https://en.wikipedia.org/wiki/Permutation#Cycle_notation

        >>> str(Permutation(2, 5, 4, 3, 1))
        '(1 2 5)(3 4)'

        :meta autosection: properties
        """
        return (
            "".join("(" + " ".join(map(str, cyc)) + ")" for cyc in self.to_cycles())
            or "1"
        )

    @classmethod
    def parse(cls, s: str) -> Permutation:
        """
        Parse a permutation written in cycle notation.  This is the inverse of
        `__str__`.

        :param str s: a permutation written in cycle notation
        :return: the permutation represented by ``s``
        :rtype: Permutation
        :meta autosection: construction
        :raises ValueError: if ``s`` is not valid cycle notation for a
            permutation
        """
        s = s.strip()
        if s == "1":
            return cls()
        if not (s.startswith("(") and s.endswith(")")):
            raise ValueError(s)
        cycles = []
        for cyc in re.split(r"\)[\s,]*\(", s[1:-1]):
            cyc = cyc.strip()
            if cyc:
                cycles.append(map(int, re.split(r"\s*,\s*|\s+", cyc)))
        return cls.from_cycles(*cycles)

    def __bool__(self) -> bool:
        """
        A `Permutation` is true iff it is not the identity.

        :meta autosection: properties
        """
        return self.__map != ()

    def __eq__(self, other: Any) -> bool:
        if type(self) is type(other):
            return bool(self.__map == other.__map)
        else:
            return NotImplemented

    def __hash__(self) -> int:
        return hash(self.__map)

    def inverse(self) -> Permutation:
        """
        Returns the inverse of the permutation.  This is the unique permutation
        that, when multiplied by the invocant on either the left or the right,
        produces the identity.

        :rtype: Permutation
        :meta autosection: properties
        """
        return type(self)(*self.permute(range(1, self.degree + 1)))

    @property
    def degree(self) -> int:
        """
        The degree of the permutation.  This is the largest integer that it
        permutes (does not map to itself), or 0 if there is no such integer
        (i.e., if the permutation is the identity).

        :meta autosection: properties
        """
        return len(self.__map)

    @property
    def order(self) -> int:
        """
        The order_/period of the permutation.  This is the smallest positive
        integer :math:`n` such that multiplying :math:`n` copies of the
        permutation together produces the identity

        .. _order: https://en.wikipedia.org/wiki/Order_(group_theory)

        :meta autosection: properties
        """
        return reduce(lcm, map(len, self.to_cycles()), 1)

    @property
    def is_even(self) -> bool:
        """
        Whether the permutation is even.  That is, whether it can be expressed
        as the product of an even number of transpositions (cycles of length
        2).

        :meta autosection: properties
        """
        return not sum((len(cyc) - 1 for cyc in self.to_cycles()), 0) % 2

    @property
    def is_odd(self) -> bool:
        """
        Whether the permutation is odd, i.e., not even

        :meta autosection: properties
        """
        return not self.is_even

    @property
    def sign(self) -> int:
        """
        The sign/signature of the permutation.  This is 1 if the permutation is
        even, -1 if it is odd.

        :meta autosection: properties
        """
        return 1 if self.is_even else -1

    def isdisjoint(self, other: Permutation) -> bool:
        """
        Tests whether the permutation is disjoint from ``other``.  This returns
        `True` iff the two permutations do not permute any of the same
        integers.

        :param Permutation other: a permutation to compare against
        :rtype: bool
        :meta autosection: properties
        """
        return all(
            i + 1 in (a, b) for (i, (a, b)) in enumerate(zip(self.__map, other.__map))
        )

    def to_image(self, n: Optional[int] = None) -> tuple[int, ...]:
        """
        Returns the images of 1 through ``n`` under the permutation.  If ``v =
        p.to_image()``, then ``v[0] == p(1)``, ``v[1] == p(2)``, etc.

        When the permutation is the identity, `to_image` called without an
        argument returns an empty tuple.

        This is the inverse of the constructor.

        :param int n: the length of the image to return; defaults to `degree`
        :return: the image of 1 through ``n`` under the permutation
        :rtype: tuple[int, ...]
        :raise ValueError: if ``n`` is less than `degree`
        :meta autosection: properties
        """
        if n is not None and n < self.degree:
            raise ValueError(n)
        return self.__map + tuple(range(self.degree + 1, (n or self.degree) + 1))

    def to_cycles(self) -> list[tuple[int, ...]]:
        """
        Decompose the permutation into a product of disjoint cycles.
        `to_cycles()` returns a list of cycles, each one represented as a tuple
        of integers.  Each cycle ``c`` is a sub-permutation that maps ``c[0]``
        to ``c[1]``, ``c[1]`` to ``c[2]``, etc., finally mapping ``c[-1]`` back
        around to ``c[0]``.  The product of these cycles is then the original
        permutation.

        Each cycle is at least two elements in length and places its smallest
        element first.  Cycles are ordered by their first elements in
        increasing order.  No two cycles share an element.

        When the permutation is the identity, `to_cycles()` returns an empty
        list.

        This is the inverse of `from_cycles`.

        :return: the cycle decomposition of the permutation
        :meta autosection: properties
        """
        cmap = list(self.__map)
        cycles = []
        for i in range(len(cmap)):
            if cmap[i] not in (0, i + 1):
                x = i + 1
                cyke = []
                while True:
                    cyke.append(x)
                    cmap[x - 1], x = 0, cmap[x - 1]
                    if x == i + 1:
                        break
                cycles.append(tuple(cyke))
        return cycles

    @classmethod
    def cycle(cls, *cyc: int) -> Permutation:
        """
        Construct a `cyclic permutation`_.  If ``p = Permutation.cycle(*cyc)``,
        then ``p(cyc[0]) == cyc[1]``, ``p(cyc[1]) == cyc[2]``, etc., and
        ``p(cyc[-1]) == cyc[0]``, with ``p`` returning all other values
        unchanged.

        ``Permutation.cycle()`` (with no arguments) evaluates to the identity
        permutation.

        .. _cyclic permutation: https://en.wikipedia.org/wiki/Cyclic_permutation

        :param cyc: zero or more distinct positive integers
        :return: the permutation represented by the given cycle
        :meta autosection: construction
        :raises ValueError:
            - if ``cyc`` contains a value less than 1
            - if ``cyc`` contains the same value more than once
        """
        cyclist = list(cyc)
        mapping = {}
        maxVal = 0
        for i, v in enumerate(cyclist):
            if v < 1:
                raise ValueError("values must be positive")
            if v in mapping:
                raise ValueError(f"{v} appears more than once in cycle")
            mapping[v] = cyclist[i + 1] if i < len(cyclist) - 1 else cyclist[0]
            if v > maxVal:
                maxVal = v
        return cls(*(mapping.get(i, i) for i in range(1, maxVal + 1)))

    @classmethod
    def from_cycles(cls, *cycles: Iterable[int]) -> Permutation:
        """
        Construct the product of cyclic permutations.  Each element of
        ``cycles`` is converted to a `Permutation` with `cycle`, and the
        results (which need not be disjoint) are multiplied together.
        ``Permutation.from_cycles()`` (with no arguments) evaluates to the
        identity permutation.

        This is the inverse of `to_cycles`.

        :param cycles: zero or more iterables of distinct positive integers
        :return: the `Permutation` represented by the product of the cycles
        :meta autosection: construction
        :raises ValueError:
            - if any cycle contains a value less than 1
            - if any cycle contains the same value more than once
        """
        return reduce(operator.mul, starmap(cls.cycle, cycles), cls())

    def right_inversion_count(self, n: Optional[int] = None) -> list[int]:
        """
        Calculate the `right inversion count`_ through degree ``n``.  The
        result is a list of ``n`` elements in which the element at index ``i``
        corresponds to the number of right inversions for ``i+1``, i.e., the
        number of values ``x > i+1`` for which ``p(x) < p(i+1)``.

        Setting ``n`` larger than `degree` causes the resulting list to have
        trailing zeroes, which become relevant when converting to & from Lehmer
        codes and factorial base.

        .. _right inversion count:
           https://en.wikipedia.org/wiki/Inversion_(discrete_mathematics)
           #Inversion_related_vectors

        .. versionadded:: 0.2.0

        :param Optional[int] n: defaults to `degree`
        :rtype: list[int]
        :raises ValueError: if ``n`` is less than `degree`
        :meta autosection: properties
        """
        if n is None:
            m = self.degree
        elif n < self.degree:
            raise ValueError(n)
        else:
            m = n
        left = list(range(1, m + 1))
        digits = []
        for x in left[:]:
            i = left.index(self(x))
            del left[i]
            digits.append(i)
        return digits

    def inversions(self) -> int:
        """
        Calculate the `inversion number`_ of the permutation.  This is the
        number of pairs of numbers which are in the opposite order after
        applying the permutation.  This is also the Kendall tau distance from
        the identity permutation.  This is also the sum of the terms in the
        Lehmer code when in factorial base.

        .. _Inversion number:
           https://en.wikipedia.org/wiki/Inversion_(discrete_mathematics)
           #Inversion_number

        .. versionadded:: 0.2.0

        :return: the number of inversions in the permutation
        :rtype: int
        :meta autosection: properties
        """
        return sum(self.right_inversion_count())

    def lehmer(self, n: int) -> int:
        """
        Calculate a `Lehmer code`_ for the permutation.  The Lehmer code is
        computed with respect to all permutations of degree at most ``n`` and
        evaluates to the zero-based index of the permutation in the list of all
        such permutations when ordered lexicographically by word
        representation.

        This is the inverse of `from_lehmer`.

        .. _Lehmer code: https://en.wikipedia.org/wiki/Lehmer_code

        :param int n:
        :rtype: int
        :raises ValueError: if ``n`` is less than `degree`
        :meta autosection: properties
        """
        return from_factorial_base(self.right_inversion_count(n)[:-1])

    @classmethod
    def from_lehmer(cls, x: int, n: int) -> Permutation:
        """
        Calculate the permutation in :math:`S_n` with Lehmer code ``x``.  This
        is the permutation at index ``x`` (zero-based) in the list of all
        permutations of degree at most ``n`` ordered lexicographically by word
        representation.

        This is the inverse of `lehmer`.

        :meta autosection: construction
        :param int x: a nonnegative integer
        :param int n: the degree of the symmetric group with respect to which
            ``x`` was calculated
        :return: the `Permutation` with Lehmer code ``x``
        :raises ValueError: if ``x`` is less than 0 or greater than or equal to
            the factorial of ``n``
        """
        if x < 0:
            raise ValueError(x)
        mapping: list[int] = []
        x2 = x
        for i in range(1, n + 1):
            x2, c = divmod(x2, i)
            for j, y in enumerate(mapping):
                if y >= c:
                    mapping[j] += 1
            mapping.insert(0, c)
        if x2 != 0:
            raise ValueError(x)
        return cls(*(c + 1 for c in mapping))

    def left_lehmer(self) -> int:
        """
        Calculate the "left Lehmer code" for the permutation.  This uses a
        modified form of `Lehmer codes <Lehmer code_>`_ that uses the `left
        inversion count`_ instead of the right inversion count.  This modified
        encoding establishes a degree-independent bijection between
        permutations and nonnegative integers, with `from_left_lehmer()`
        converting values in the opposite direction.

        .. _left inversion count:
           https://en.wikipedia.org/wiki/Inversion_(discrete_mathematics)
           #Inversion_related_vectors

        :return: the permutation's left Lehmer code
        :rtype: int
        :meta autosection: properties
        """
        left = list(range(self.degree, 0, -1))
        digits = []
        for x in left[:]:
            i = left.index(self(x))
            del left[i]
            digits.append(i)
        return from_factorial_base(digits[:-1])

    @classmethod
    def from_left_lehmer(cls, x: int) -> Permutation:
        """
        Calculate the permutation with the given left Lehmer code.  This is the
        inverse of `left_lehmer()`.

        :param int x: a nonnegative integer
        :return: the `Permutation` with left Lehmer code ``x``
        :raises ValueError: if ``x`` is less than 0
        :meta autosection: construction
        """
        if x < 0:
            raise ValueError(x)
        mapping = [0]
        for c in reversed(to_factorial_base(x)):
            for i, y in enumerate(mapping):
                if y >= c:
                    mapping[i] += 1
            mapping.append(c)
        return cls(*(len(mapping) - c for c in mapping))

    @classmethod
    def group(cls, n: int) -> Iterator[Permutation]:
        """
        Generates all permutations in :math:`S_n`.  This is the symmetric group
        of degree ``n``, i.e., all permutations with degree less than or equal
        to ``n``.  The permutations are yielded in ascending order of their
        `left Lehmer codes <#permutation.Permutation.left_lehmer>`_.

        :param int n: a nonnegative integer
        :return: a generator of all `Permutation`\\s with degree ``n`` or less
        :raises ValueError: if ``n`` is less than 0
        :meta autosection: construction
        """
        if n < 0:
            raise ValueError(n)

        # Use a nested function as the actual generator so that the ValueError
        # above can be raised immediately:
        def sn() -> Iterator[Permutation]:
            p = cls()
            while p.degree <= n:
                yield p
                p = p.next_permutation()

        return sn()

    def next_permutation(self) -> Permutation:
        """
        Returns the next `Permutation` in `left Lehmer code
        <#permutation.Permutation.left_lehmer>`_ order

        :meta autosection: construction
        """
        map2 = list(self.__map)
        for i in range(1, len(map2)):
            if map2[i] > map2[i - 1]:
                j = 0
                while map2[i] <= map2[j]:
                    j += 1
                map2[i], map2[j] = map2[j], map2[i]
                map2[:i] = reversed(map2[:i])
                return type(self)(*map2)
        d = max(self.degree, 1)
        return type(self).cycle(d, d + 1)

    def prev_permutation(self) -> Permutation:
        """
        Returns the previous `Permutation` in `left Lehmer code
        <#permutation.Permutation.left_lehmer>`_ order

        :meta autosection: construction
        :raises ValueError: if called on the identity `Permutation` (which has
            no predecessor)
        """
        if self.degree < 2:
            raise ValueError("cannot decrement identity")
        map2 = list(self.__map)
        for i in range(1, len(map2)):
            if map2[i] < map2[i - 1]:
                j = 0
                while map2[i] >= map2[j]:
                    j += 1
                map2[i], map2[j] = map2[j], map2[i]
                map2[:i] = reversed(map2[:i])
                return type(self)(*map2)
        raise AssertionError("Unreachable state reached")  # pragma: no cover

    def permute(self, xs: Iterable[T]) -> list[T]:
        """
        Returns the elements of ``xs`` reordered according to the permutation.
        Each element at index ``i`` is moved to index ``p(i)``.

        Note that ``p.permute(range(1, n+1)) == p.inverse().to_image(n)`` for
        all integers ``n`` greater than or equal to `degree`.

        .. versionchanged:: 0.5.0

            This method now accepts iterables of any element type and returns a
            list.  (Previously, it only accepted iterables of `int`\\s and
            returned a tuple.)

        :param xs: a sequence of at least `degree` elements
        :return: a permuted sequence
        :rtype: list
        :raise ValueError: if ``len(xs)`` is less than `degree`
        :meta autosection: operations
        """
        xs = list(xs)
        if len(xs) < self.degree:
            raise ValueError("sequence must have at least `degree` elements")
        out: list[Optional[T]] = [None] * len(xs)
        for i in range(len(xs)):
            out[self(i + 1) - 1] = xs[i]
        return cast(List[T], out)


def lcm(x: int, y: int) -> int:
    """Calculate the least common multiple of ``x`` and ``y``"""
    d = gcd(x, y)
    return 0 if d == 0 else abs(x * y) // d


def to_factorial_base(n: int) -> list[int]:
    """
    Convert a nonnegative integer to its representation in the `factorial
    number system <https://en.wikipedia.org/wiki/Factorial_number_system>`_
    (represented as a list of digits in descending order of place value, not
    including the final zero digit sometimes appended for the :math:`0!` place)
    """
    if n < 0:
        raise ValueError(n)
    if n == 0:
        return [0]
    digits = []
    i = 1
    while n > 0:
        digits.append(n % (i + 1))
        i += 1
        n //= i
    digits.reverse()
    return digits


def from_factorial_base(digits: Sequence[int]) -> int:
    """Inverse of `to_factorial_base`"""
    n = 0
    base = 1
    for i, d in enumerate(reversed(digits), start=1):
        if not (0 <= d <= i):
            raise ValueError(digits)
        n += d * base
        base *= i + 1
    return n
