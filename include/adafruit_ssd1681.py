# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`adafruit_ssd1681`
================================================================================

CircuitPython `displayio` driver for SSD1681-based ePaper displays


* Author(s): Melissa LeBlanc-Williams

Implementation Notes
--------------------

**Hardware:**

* `Adafruit 1.54" Tri-Color Display Breakout <https://www.adafruit.com/product/4868>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware (version 5+) for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

import displayio

__version__ = "1.0.7"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_SSD1681.git"

_START_SEQUENCE = (
    b"\x12\x80\x14"  # soft reset and wait 20ms
    b"\x11\x01\x03"  # Ram data entry mode
    b"\x3C\x01\x05"  # border color
    b"\x18\x01\x80"  # Temp control
    b"\x4e\x01\x00"  # ram x count
    b"\x4f\x02\x00\x00"  # ram y count
    b"\x01\x03\x00\x00\x00"  # set display size
    b"\x22\x01\xf7"  # only do full screen updates
)

_STOP_SEQUENCE = b"\x10\x81\x01\x64"  # Deep Sleep
# pylint: disable=too-few-public-methods
class SSD1681(displayio.EPaperDisplay):
    r"""SSD1681 driver

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
        start_sequence = bytearray(_START_SEQUENCE)

        width = kwargs["width"]
        height = kwargs["height"]
        if "rotation" in kwargs and kwargs["rotation"] % 180 != 0:
            width, height = height, width
        start_sequence[21] = (width - 1) & 0xFF
        start_sequence[22] = ((width >> 8) - 1) & 0xFF

        super().__init__(
            bus,
            start_sequence,
            _STOP_SEQUENCE,
            **kwargs,
            ram_width=200,
            ram_height=296,
            busy_state=True,
            write_black_ram_command=0x24,
            write_color_ram_command=0x26,
            black_bits_inverted=False,
            set_column_window_command=0x44,
            set_row_window_command=0x45,
            set_current_column_command=0x4E,
            set_current_row_command=0x4F,
            refresh_display_command=0x20,
            always_toggle_chip_select=True,
        )
