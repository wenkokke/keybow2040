"""Numerical approximation methods"""

from __future__ import annotations

from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, Union

import ulab

def interp(
    x: ulab.numpy.ndarray,
    xp: ulab.numpy.ndarray,
    fp: ulab.numpy.ndarray,
    *,
    left: Optional[_float] = None,
    right: Optional[_float] = None
) -> ulab.numpy.ndarray:
    """
    :param ulab.numpy.ndarray x: The x-coordinates at which to evaluate the interpolated values.
    :param ulab.numpy.ndarray xp: The x-coordinates of the data points, must be increasing
    :param ulab.numpy.ndarray fp: The y-coordinates of the data points, same length as xp
    :param left: Value to return for ``x < xp[0]``, default is ``fp[0]``.
    :param right: Value to return for ``x > xp[-1]``, default is ``fp[-1]``.

    Returns the one-dimensional piecewise linear interpolant to a function with given discrete data points (xp, fp), evaluated at x."""
    ...

def trapz(
    y: ulab.numpy.ndarray, x: Optional[ulab.numpy.ndarray] = None, dx: _float = 1.0
) -> _float:
    """
    :param 1D ulab.numpy.ndarray y: the values of the dependent variable
    :param 1D ulab.numpy.ndarray x: optional, the coordinates of the independent variable. Defaults to uniformly spaced values.
    :param float dx: the spacing between sample points, if x=None

    Returns the integral of y(x) using the trapezoidal rule.
    """
    ...

"""Numerical and Statistical functions

Most of these functions take an "axis" argument, which indicates whether to
operate over the flattened array (None), or a particular axis (integer)."""

from typing import Dict

_ArrayLike = Union[ndarray, List[_float], Tuple[_float], range]

_DType = int
"""`ulab.numpy.int8`, `ulab.numpy.uint8`, `ulab.numpy.int16`, `ulab.numpy.uint16`, `ulab.numpy.float` or `ulab.numpy.bool`"""

_float = float
"""Type alias of the bulitin float"""

_bool = bool
"""Type alias of the bulitin bool"""

int8: _DType
"""Type code for signed integers in the range -128 .. 127 inclusive, like the 'b' typecode of `array.array`"""

int16: _DType
"""Type code for signed integers in the range -32768 .. 32767 inclusive, like the 'h' typecode of `array.array`"""

float: _DType
"""Type code for floating point values, like the 'f' typecode of `array.array`"""

uint8: _DType
"""Type code for unsigned integers in the range 0 .. 255 inclusive, like the 'H' typecode of `array.array`"""

uint16: _DType
"""Type code for unsigned integers in the range 0 .. 65535 inclusive, like the 'h' typecode of `array.array`"""

bool: _DType
"""Type code for boolean values"""

def argmax(array: _ArrayLike, *, axis: Optional[int] = None) -> int:
    """Return the index of the maximum element of the 1D array"""
    ...

def argmin(array: _ArrayLike, *, axis: Optional[int] = None) -> int:
    """Return the index of the minimum element of the 1D array"""
    ...

def argsort(array: ulab.numpy.ndarray, *, axis: int = -1) -> ulab.numpy.ndarray:
    """Returns an array which gives indices into the input array from least to greatest."""
    ...

def cross(a: ulab.numpy.ndarray, b: ulab.numpy.ndarray) -> ulab.numpy.ndarray:
    """Return the cross product of two vectors of length 3"""
    ...

def diff(
    array: ulab.numpy.ndarray, *, n: int = 1, axis: int = -1
) -> ulab.numpy.ndarray:
    """Return the numerical derivative of successive elements of the array, as
    an array.  axis=None is not supported."""
    ...

def flip(
    array: ulab.numpy.ndarray, *, axis: Optional[int] = None
) -> ulab.numpy.ndarray:
    """Returns a new array that reverses the order of the elements along the
    given axis, or along all axes if axis is None."""
    ...

def max(array: _ArrayLike, *, axis: Optional[int] = None) -> _float:
    """Return the maximum element of the 1D array"""
    ...

def mean(array: _ArrayLike, *, axis: Optional[int] = None) -> _float:
    """Return the mean element of the 1D array, as a number if axis is None, otherwise as an array."""
    ...

def median(array: ulab.numpy.ndarray, *, axis: int = -1) -> ulab.numpy.ndarray:
    """Find the median value in an array along the given axis, or along all axes if axis is None."""
    ...

def min(array: _ArrayLike, *, axis: Optional[int] = None) -> _float:
    """Return the minimum element of the 1D array"""
    ...

def roll(
    array: ulab.numpy.ndarray, distance: int, *, axis: Optional[int] = None
) -> None:
    """Shift the content of a vector by the positions given as the second
    argument. If the ``axis`` keyword is supplied, the shift is applied to
    the given axis.  The array is modified in place."""
    ...

def sort(array: ulab.numpy.ndarray, *, axis: int = -1) -> ulab.numpy.ndarray:
    """Sort the array along the given axis, or along all axes if axis is None.
    The array is modified in place."""
    ...

def std(array: _ArrayLike, *, axis: Optional[int] = None, ddof: int = 0) -> _float:
    """Return the standard deviation of the array, as a number if axis is None, otherwise as an array."""
    ...

def sum(
    array: _ArrayLike, *, axis: Optional[int] = None
) -> Union[_float, int, ulab.numpy.ndarray]:
    """Return the sum of the array, as a number if axis is None, otherwise as an array."""
    ...

"""Compatibility layer for numpy"""

class ndarray: ...

def get_printoptions() -> Dict[str, int]:
    """Get printing options"""
    ...

def set_printoptions(
    threshold: Optional[int] = None, edgeitems: Optional[int] = None
) -> None:
    """Set printing options"""
    ...

def ndinfo(array: ulab.numpy.ndarray) -> None: ...
def array(
    values: Union[ndarray, Iterable[Union[_float, _bool, Iterable[Any]]]],
    *,
    dtype: _DType = ulab.numpy.float
) -> ulab.numpy.ndarray:
    """alternate constructor function for `ulab.numpy.ndarray`. Mirrors numpy.array"""
    ...

def trace(m: ulab.numpy.ndarray) -> _float:
    """
    :param m: a square matrix

    Compute the trace of the matrix, the sum of its diagonal elements."""
    ...

def dot(
    m1: ulab.numpy.ndarray, m2: ulab.numpy.ndarray
) -> Union[ulab.numpy.ndarray, _float]:
    """
    :param ~ulab.numpy.ndarray m1: a matrix, or a vector
    :param ~ulab.numpy.ndarray m2: a matrix, or a vector

    Computes the product of two matrices, or two vectors. In the letter case, the inner product is returned."""
    ...

"""Element-by-element functions

These functions can operate on numbers, 1-D iterables, and arrays of 1 to 4 dimensions by
applying the function to every element in the array.  This is typically
much more efficient than expressing the same operation as a Python loop."""

def acos(a: _ArrayLike) -> ulab.numpy.ndarray:
    """Computes the inverse cosine function"""
    ...

def acosh(a: _ArrayLike) -> ulab.numpy.ndarray:
    """Computes the inverse hyperbolic cosine function"""
    ...

def asin(a: _ArrayLike) -> ulab.numpy.ndarray:
    """Computes the inverse sine function"""
    ...

def asinh(a: _ArrayLike) -> ulab.numpy.ndarray:
    """Computes the inverse hyperbolic sine function"""
    ...

def around(a: _ArrayLike, *, decimals: int = 0) -> ulab.numpy.ndarray:
    """Returns a new float array in which each element is rounded to
    ``decimals`` places."""
    ...

def atan(a: _ArrayLike) -> ulab.numpy.ndarray:
    """Computes the inverse tangent function; the return values are in the
    range [-pi/2,pi/2]."""
    ...

def arctan2(ya: _ArrayLike, xa: _ArrayLike) -> ulab.numpy.ndarray:
    """Computes the inverse tangent function of y/x; the return values are in
    the range [-pi, pi]."""
    ...

def atanh(a: _ArrayLike) -> ulab.numpy.ndarray:
    """Computes the inverse hyperbolic tangent function"""
    ...

def ceil(a: _ArrayLike) -> ulab.numpy.ndarray:
    """Rounds numbers up to the next whole number"""
    ...

def cos(a: _ArrayLike) -> ulab.numpy.ndarray:
    """Computes the cosine function"""
    ...

def cosh(a: _ArrayLike) -> ulab.numpy.ndarray:
    """Computes the hyperbolic cosine function"""
    ...

def degrees(a: _ArrayLike) -> ulab.numpy.ndarray:
    """Converts angles from radians to degrees"""
    ...

def erf(a: _ArrayLike) -> ulab.numpy.ndarray:
    """Computes the error function, which has applications in statistics"""
    ...

def erfc(a: _ArrayLike) -> ulab.numpy.ndarray:
    """Computes the complementary error function, which has applications in statistics"""
    ...

def exp(a: _ArrayLike) -> ulab.numpy.ndarray:
    """Computes the exponent function."""
    ...

def expm1(a: _ArrayLike) -> ulab.numpy.ndarray:
    """Computes $e^x-1$.  In certain applications, using this function preserves numeric accuracy better than the `exp` function."""
    ...

def floor(a: _ArrayLike) -> ulab.numpy.ndarray:
    """Rounds numbers up to the next whole number"""
    ...

def gamma(a: _ArrayLike) -> ulab.numpy.ndarray:
    """Computes the gamma function"""
    ...

def lgamma(a: _ArrayLike) -> ulab.numpy.ndarray:
    """Computes the natural log of the gamma function"""
    ...

def log(a: _ArrayLike) -> ulab.numpy.ndarray:
    """Computes the natural log"""
    ...

def log10(a: _ArrayLike) -> ulab.numpy.ndarray:
    """Computes the log base 10"""
    ...

def log2(a: _ArrayLike) -> ulab.numpy.ndarray:
    """Computes the log base 2"""
    ...

def radians(a: _ArrayLike) -> ulab.numpy.ndarray:
    """Converts angles from degrees to radians"""
    ...

def sin(a: _ArrayLike) -> ulab.numpy.ndarray:
    """Computes the sine function"""
    ...

def sinh(a: _ArrayLike) -> ulab.numpy.ndarray:
    """Computes the hyperbolic sine"""
    ...

def sqrt(a: _ArrayLike) -> ulab.numpy.ndarray:
    """Computes the square root"""
    ...

def tan(a: _ArrayLike) -> ulab.numpy.ndarray:
    """Computes the tangent"""
    ...

def tanh(a: _ArrayLike) -> ulab.numpy.ndarray:
    """Computes the hyperbolic tangent"""
    ...

def vectorize(
    f: Union[Callable[[int], _float], Callable[[_float], _float]],
    *,
    otypes: Optional[_DType] = None
) -> Callable[[_ArrayLike], ulab.numpy.ndarray]:
    """
    :param callable f: The function to wrap
    :param otypes: List of array types that may be returned by the function.  None is interpreted to mean the return value is float.

    Wrap a Python function ``f`` so that it can be applied to arrays.
    The callable must return only values of the types specified by ``otypes``, or the result is undefined."""
    ...
