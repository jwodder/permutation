.. image:: http://www.repostatus.org/badges/latest/active.svg
    :target: http://www.repostatus.org/#active
    :alt: Project Status: Active — The project has reached a stable, usable
          state and is being actively developed.

.. image:: https://github.com/jwodder/permutation/workflows/Test/badge.svg?branch=master
    :target: https://github.com/jwodder/permutation/actions?workflow=Test
    :alt: CI Status

.. image:: https://codecov.io/gh/jwodder/permutation/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jwodder/permutation

.. image:: https://img.shields.io/pypi/pyversions/permutation.svg
    :target: https://pypi.org/project/permutation

.. image:: https://img.shields.io/github/license/jwodder/permutation.svg
    :target: https://opensource.org/licenses/MIT
    :alt: MIT License

`GitHub <https://github.com/jwodder/permutation>`_
| `PyPI <https://pypi.org/project/permutation>`_
| `Documentation <https://permutation.readthedocs.io>`_
| `Issues <https://github.com/jwodder/permutation/issues>`_
| `Changelog <https://github.com/jwodder/permutation/blob/master/CHANGELOG.md>`_

``permutation`` provides a ``Permutation`` class for representing `permutations
<https://en.wikipedia.org/wiki/Permutation>`_ of finitely many positive
integers in Python.  Supported operations & properties include inverses, (group
theoretic) order, parity, composition/multiplication, cycle decomposition,
cycle notation, word representation, Lehmer codes, and, of course, use as a
callable on integers.


Installation
============
``permutation`` requires Python 3.7 or higher.  Just use `pip
<https://pip.pypa.io>`_ for Python 3 (You have pip, right?) to install::

    python3 -m pip install permutation


Examples
========

>>> from permutation import Permutation
>>> p = Permutation(2, 1, 4, 5, 3)
>>> p.to_cycles()
[(1, 2), (3, 4, 5)]
>>> print(p)
(1 2)(3 4 5)
>>> print(p.inverse())
(1 2)(3 5 4)
>>> p.degree
5
>>> p.order
6
>>> p.is_even
False
>>> p.lehmer(5)
27
>>> q = Permutation.cycle(1,2,3)
>>> print(p * q)
(2 4 5 3)
>>> print(q * p)
(1 3 4 5)
>>> for p in Permutation.group(3):
...     print(p)
...
1
(1 2)
(2 3)
(1 3 2)
(1 2 3)
(1 3)
