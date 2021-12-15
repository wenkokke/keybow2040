# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`adafruit_uc8151d`
================================================================================

CircuitPython `displayio` driver for US8151D-based ePaper displays


* Author(s): Melissa LeBlanc-Williams

Implementation Notes
--------------------

**Hardware:**

* `Adafruit Flexible 2.9" Black and White <https://www.adafruit.com/product/4262>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

import displayio

__version__ = "1.0.1"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_UC8151D.git"

_START_SEQUENCE = (
    # b"\x01\x05\x03\x00\x2b\x2b\x09"  # power setting
    # b"\x06\x03\x17\x17\x17"  # booster soft start
    b"\x04\x80\xc8"  # power on and wait 10 ms
    b"\x00\x01\x1f"  # panel setting. Further filled in below.
    b"\x50\x01\x97"  # CDI setting
)

_STOP_SEQUENCE = b"\x50\x01\xf7" b"\x07\x01\xA5"  # CDI setting  # Deep Sleep
# pylint: disable=too-few-public-methods
class UC8151D(displayio.EPaperDisplay):
    r"""UC8151D driver

    :param bus: The data bus the display is on
    :param \**kwargs:
        See below

    :Keyword Arguments:
        * *width* (``int``) --
          Display width
        * *height* (``int``) --
          Display height
        * *rotation* (``int``) --
          Display rotation
    """

    def __init__(self, bus, **kwargs):
        width = kwargs["width"]
        height = kwargs["height"]
        if "rotation" in kwargs and kwargs["rotation"] % 180 != 0:
            width, height = height, width

        super().__init__(
            bus,
            _START_SEQUENCE,
            _STOP_SEQUENCE,
            **kwargs,
            ram_width=128,
            ram_height=296,
            busy_state=False,
            write_black_ram_command=0x13,
            write_color_ram_command=0x10,
            refresh_display_command=0x12,
        )
