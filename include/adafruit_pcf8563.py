# SPDX-FileCopyrightText: 2016 Philip R. Moyer and Radomir Dopieralski for Adafruit Industries.
# SPDX-FileCopyrightText: Copyright (c) 2021 Jeff Epler for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_pcf8563` - PCF8563 Real Time Clock module
====================================================

This library supports the use of the PCF8563-based RTC in CircuitPython. It
contains a base RTC class used by all Adafruit RTC libraries. This base
class is inherited by the chip-specific subclasses.

Functions are included for reading and writing registers and manipulating
datetime objects.

Author(s): Philip R. Moyer and Radomir Dopieralski for Adafruit Industries.
Date: November 2016
Affiliation: Adafruit Industries

Implementation Notes
--------------------

**Hardware:**

* `Seeeduino XIAO Expansion Board <https://www.adafruit.com/product/5033>`_
  - Works With Adafruit QT Py (Product ID: 5033)

**Software and Dependencies:**

* Adafruit CircuitPython firmware: https://github.com/adafruit/circuitpython/releases
* Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register
* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice

**Notes:**

#. Milliseconds are not supported by this RTC.
#. Datasheet: http://cache.nxp.com/documents/data_sheet/PCF8563.pdf

"""

__version__ = "1.0.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_PCF8563.git"

import time

from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_register import i2c_bit
from adafruit_register import i2c_bcd_alarm
from adafruit_register import i2c_bcd_datetime


class PCF8563:
    """Interface to the PCF8563 RTC."""

    datetime_compromised = i2c_bit.RWBit(0x2, 7)
    """True if the clock integrity is compromised."""

    # The False means that day comes before weekday in the registers. The 0 is
    # that the first day of the week is value 0 and not 1.
    datetime_register = i2c_bcd_datetime.BCDDateTimeRegister(0x02, False, 0)
    """Current date and time."""

    # The False means that day and weekday share a register. The 0 is that the
    # first day of the week is value 0 and not 1.
    alarm = i2c_bcd_alarm.BCDAlarmTimeRegister(
        0x09, has_seconds=False, weekday_shared=False, weekday_start=0
    )
    """Alarm time for the alarm."""

    alarm_interrupt = i2c_bit.RWBit(0x01, 1)
    """True if the interrupt pin will output when alarm is alarming."""

    alarm_status = i2c_bit.RWBit(0x01, 3)
    """True if alarm is alarming. Set to False to reset."""

    def __init__(self, i2c_bus):
        time.sleep(0.05)
        self.i2c_device = I2CDevice(i2c_bus, 0x51)

        # Try and verify this is the RTC we expect by checking the timer B
        # frequency control bits which are 1 on reset and shouldn't ever be
        # changed.
        buf = bytearray(2)
        buf[0] = 0x12
        with self.i2c_device as i2c:
            i2c.write_then_readinto(buf, buf, out_end=1, in_start=1)

    @property
    def datetime(self):
        """Gets the current date and time or sets the current date and time then starts the
        clock."""
        return self.datetime_register

    @datetime.setter
    def datetime(self, value):
        # Automatically sets lost_power to false.
        self.datetime_register = value
        self.datetime_compromised = False
