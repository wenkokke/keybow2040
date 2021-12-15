"""Manipulate numeric data similar to numpy

`ulab` is a numpy-like module for micropython, meant to simplify and
speed up common mathematical operations on arrays. The primary goal was to
implement a small subset of numpy that might be useful in the context of a
microcontroller. This means low-level data processing of linear (array) and
two-dimensional (matrix) data.

`ulab` is adapted from micropython-ulab, and the original project's
documentation can be found at
https://micropython-ulab.readthedocs.io/en/latest/

`ulab` is modeled after numpy, and aims to be a compatible subset where
possible.  Numpy's documentation can be found at
https://docs.scipy.org/doc/numpy/index.html"""

from __future__ import annotations

from typing import Union

from .numpy import ndarray as _ndarray

ndarray = Union[_ndarray]
"""A temporary alias for the type `ulab.numpy.ndarray` needed during a transitional period. Do not use."""
