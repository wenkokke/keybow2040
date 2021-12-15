"""USB Human Interface Device

The `usb_hid` module allows you to output data as a HID device."""

from __future__ import annotations

from typing import Optional, Sequence, Tuple

from _typing import ReadableBuffer

devices: Tuple[Device, ...]
"""Tuple of all active HID device interfaces.
The default set of devices is ``Device.KEYBOARD, Device.MOUSE, Device.CONSUMER_CONTROL``,
On boards where `usb_hid` is disabled by default, `devices` is an empty tuple.
"""

def disable() -> None:
    """Do not present any USB HID devices to the host computer.
    Can be called in ``boot.py``, before USB is connected.
    The HID composite device is normally enabled by default,
    but on some boards with limited endpoints, including STM32F4,
    it is disabled by default. You must turn off another USB device such
    as `usb_cdc` or `storage` to free up endpoints for use by `usb_hid`.
    """

def enable(devices: Optional[Sequence[Device]]) -> None:
    """Specify which USB HID devices that will be available.
    Can be called in ``boot.py``, before USB is connected.

    :param Sequence devices: `Device` objects.
      If `devices` is empty, HID is disabled. The order of the ``Devices``
      may matter to the host. For instance, for MacOS, put the mouse device
      before any Gamepad or Digitizer HID device or else it will not work.

    If you enable too many devices at once, you will run out of USB endpoints.
    The number of available endpoints varies by microcontroller.
    CircuitPython will go into safe mode after running boot.py to inform you if
    not enough endpoints are available.
    """
    ...

class Device:
    """HID Device specification"""

    def __init__(
        self,
        *,
        descriptor: ReadableBuffer,
        usage_page: int,
        usage: int,
        in_report_length: int,
        out_report_length: int = 0,
        report_id_index: Optional[int]
    ) -> None:
        """Create a description of a USB HID device. The actual device is created when you
        pass a `Device` to `usb_hid.enable()`.

        :param ReadableBuffer report_descriptor: The USB HID Report descriptor bytes. The descriptor is not
          not verified for correctness; it is up to you to make sure it is not malformed.
        :param int usage_page: The Usage Page value from the descriptor. Must match what is in the descriptor.
        :param int usage: The Usage value from the descriptor. Must match what is in the descriptor.
        :param int in_report_length: Size in bytes of the HID report sent to the host.
          "In" is with respect to the host.
        :param int out_report_length: Size in bytes of the HID report received from the host.
          "Out" is with respect to the host. If no reports are expected, use 0.
        :param int report_id_index: position of byte in descriptor that contains the Report ID.
          A Report ID will be assigned when the device is created. If there is no
          Report ID, use ``None``.
        """
        ...
    KEYBOARD: Device
    """Standard keyboard device supporting keycodes 0x00-0xDD, modifiers 0xE-0xE7, and five LED indicators."""

    MOUSE: Device
    """Standard mouse device supporting five mouse buttons, X and Y relative movements from -127 to 127
    in each report, and a relative mouse wheel change from -127 to 127 in each report."""

    CONSUMER_CONTROL: Device
    """Consumer Control device supporting sent values from 1-652, with no rollover."""
    def send_report(self, buf: ReadableBuffer) -> None:
        """Send a HID report."""
        ...
    last_received_report: bytes
    """The HID OUT report as a `bytes`. (read-only). `None` if nothing received."""

    usage_page: int
    """The usage page of the device as an `int`. Can be thought of a category. (read-only)"""

    usage: int
    """The functionality of the device as an int. (read-only)

    For example, Keyboard is 0x06 within the generic desktop usage page 0x01.
    Mouse is 0x02 within the same usage page."""
