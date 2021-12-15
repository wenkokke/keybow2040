# SPDX-FileCopyrightText: Copyright (c) 2021 Dan Halbert for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`adafruit_radial_controller`
================================================================================

HID Radial Controller device helper library


* Author(s): Dan Halbert

Implementation Notes
--------------------

**Hardware:**

  At the minimum, a radial controller is a rotary encoder plus a switch.

  Documentation is available from Microsoft:
  https://docs.microsoft.com/en-us/windows-hardware/design/component-guidelines/radial-implementation-guide

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases
"""
import time

import usb_hid
from adafruit_hid import find_device

__version__ = "1.0.2"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_Radial_Controller.git"


class RadialController:
    """Send Radial Controller HID reports."""

    def __init__(self, devices):
        """Create a RadialController object that will send Radial Controller HID reports.

        Devices can be a list of devices that includes a keyboard device or a keyboard device
        itself. A device is any object that implements ``send_report()``, ``usage_page`` and
        ``usage``.
        """
        self._controller = find_device(devices, usage_page=0x01, usage=0x0E)

        # Reuse this bytearray to send radial controller reports
        # report[0]: bit 0: button
        # report[1]: rotation
        self.report = bytearray(3)

        self._pressed = False

        # Do a no-op to test if HID device is ready.
        # If not, wait a bit and try once more.
        try:
            self._send(False, 0)
        except OSError:
            time.sleep(1)
            self._send(False, 0)

    def press(self):
        """Press the button."""
        self._pressed = True
        self._send(True, 0)

    def release(self):
        """Release the button."""
        self._pressed = False
        self._send(False, 0)

    def click(self):
        """Press and release the button."""
        self.press()
        self.release()

    def rotate(self, degree_tenths):
        """Set relative rotation value, in tenths of a degree.
        A value of +/- 1 or 10 can be too small and cause tool selection or scrolling to not work.
        +/- 100 is a good value for a single increment in many cases, though it causes value sliders
        to change by 10 instead of 1.
        """

        if not -3600 <= degree_tenths <= 3600:
            raise ValueError("rotation must be in range -3600 to 3600")
        self._send(self._pressed, degree_tenths)

    def _send(self, pressed, rotation):
        self.report[0] = int(pressed)
        self.report[1] = rotation & 0xFF
        self.report[2] = (rotation >> 8) & 0xFF

        self._controller.send_report(self.report)
