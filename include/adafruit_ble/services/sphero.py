# SPDX-FileCopyrightText: 2019 Scott Shawcroft for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`sphero`
====================================================

This module provides Services used by Sphero robots.

"""

from . import Service
from ..uuid import VendorUUID

__version__ = "8.1.2"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_BLE.git"


class SpheroService(Service):
    """Core Sphero Service. Unimplemented."""

    uuid = VendorUUID("!!orehpS OOW\x01\x00\x01\x00")
