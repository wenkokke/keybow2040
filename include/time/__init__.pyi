"""time and timing related functions

The `time` module is a strict subset of the CPython `cpython:time` module. So, code
written in MicroPython will work in CPython but not necessarily the other
way around."""

from __future__ import annotations

from typing import Sequence

def monotonic() -> float:
    """Returns an always increasing value of time with an unknown reference
    point. Only use it to compare against other values from `monotonic`.

    :return: the current monotonic time
    :rtype: float"""
    ...

def sleep(seconds: float) -> None:
    """Sleep for a given number of seconds.

    :param float seconds: the time to sleep in fractional seconds"""
    ...

class struct_time:
    def __init__(self, time_tuple: Sequence[int]) -> None:
        """Structure used to capture a date and time.  Can be constructed from a `struct_time`, `tuple`, `list`, or `namedtuple` with 9 elements.

        :param Sequence time_tuple: Sequence of time info: ``(tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst)``

          * ``tm_year``: the year, 2017 for example
          * ``tm_mon``: the month, range [1, 12]
          * ``tm_mday``: the day of the month, range [1, 31]
          * ``tm_hour``: the hour, range [0, 23]
          * ``tm_min``: the minute, range [0, 59]
          * ``tm_sec``: the second, range [0, 61]
          * ``tm_wday``: the day of the week, range [0, 6], Monday is 0
          * ``tm_yday``: the day of the year, range [1, 366], -1 indicates not known
          * ``tm_isdst``: 1 when in daylight savings, 0 when not, -1 if unknown."""
        ...

def time() -> int:
    """Return the current time in seconds since since Jan 1, 1970.

    :return: the current time
    :rtype: int"""
    ...

def monotonic_ns() -> int:
    """Return the time of the monotonic clock, cannot go backward, in nanoseconds.

    :return: the current time
    :rtype: int"""
    ...

def localtime(secs: int) -> struct_time:
    """Convert a time expressed in seconds since Jan 1, 1970 to a struct_time in
    local time. If secs is not provided or None, the current time as returned
    by time() is used.
    The earliest date for which it can generate a time is Jan 1, 2000.

    :return: the current time
    :rtype: time.struct_time"""
    ...

def mktime(t: struct_time) -> int:
    """This is the inverse function of localtime(). Its argument is the
    struct_time or full 9-tuple (since the dst flag is needed; use -1 as the
    dst flag if it is unknown) which expresses the time in local time, not UTC.
    The earliest date for which it can generate a time is Jan 1, 2000.

    :return: seconds
    :rtype: int"""
    ...
