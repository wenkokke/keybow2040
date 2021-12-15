"""Hardware accelerated external bus access

The I2CDevice and SPIDevice helper classes make managing transaction state on a bus easy.
For example, they manage locking the bus to prevent other concurrent access. For SPI
devices, it manages the chip select and protocol changes such as mode. For I2C, it
manages the device address."""

from __future__ import annotations

from typing import Optional

import busio
import microcontroller
from _typing import ReadableBuffer, WriteableBuffer

class I2CDevice:
    """I2C Device Manager"""

    def __init__(self, i2c: busio.I2C, device_address: int, probe: bool = True) -> None:

        """Represents a single I2C device and manages locking the bus and the device
        address.

        :param ~busio.I2C i2c: The I2C bus the device is on
        :param int device_address: The 7 bit device address
        :param bool probe: Probe for the device upon object creation, default is true

        Example::

            import busio
            from board import *
            from adafruit_bus_device.i2c_device import I2CDevice
            with busio.I2C(SCL, SDA) as i2c:
                device = I2CDevice(i2c, 0x70)
                bytes_read = bytearray(4)
                with device:
                    device.readinto(bytes_read)
                # A second transaction
                with device:
                    device.write(bytes_read)"""
    ...
    def __enter__(self) -> I2CDevice:
        """Context manager entry to lock bus."""
        ...
    def __exit__(self) -> None:
        """Automatically unlocks the bus on exit."""
        ...
    def readinto(
        self, buf: WriteableBuffer, *, start: int = 0, end: Optional[int] = None
    ) -> None:
        """Read into ``buf`` from the device. The number of bytes read will be the
        length of ``buf``.
        If ``start`` or ``end`` is provided, then the buffer will be sliced
        as if ``buf[start:end]``. This will not cause an allocation like
        ``buf[start:end]`` will so it saves memory.

        :param bytearray buf: buffer to write into
        :param int start: Index to start writing at
        :param int end: Index to write up to but not include; if None, use ``len(buf)``"""
        ...
    def write(
        self, buf: ReadableBuffer, *, start: int = 0, end: Optional[int] = None
    ) -> None:
        """Write the bytes from ``buffer`` to the device, then transmit a stop bit.
        If ``start`` or ``end`` is provided, then the buffer will be sliced
        as if ``buffer[start:end]``. This will not cause an allocation like
        ``buffer[start:end]`` will so it saves memory.

        :param bytearray buf: buffer containing the bytes to write
        :param int start: Index to start writing from
        :param int end: Index to read up to but not include; if None, use ``len(buf)``
        """
        ...
    def write_then_readinto(
        self,
        out_buffer: WriteableBuffer,
        in_buffer: ReadableBuffer,
        *,
        out_start: int = 0,
        out_end: Optional[int] = None,
        in_start: int = 0,
        in_end: Optional[int] = None
    ) -> None:
        """Write the bytes from ``out_buffer`` to the device, then immediately
        reads into ``in_buffer`` from the device. The number of bytes read
        will be the length of ``in_buffer``.
        If ``out_start`` or ``out_end`` is provided, then the output buffer
        will be sliced as if ``out_buffer[out_start:out_end]``. This will
        not cause an allocation like ``buffer[out_start:out_end]`` will so
        it saves memory.
        If ``in_start`` or ``in_end`` is provided, then the input buffer
        will be sliced as if ``in_buffer[in_start:in_end]``. This will not
        cause an allocation like ``in_buffer[in_start:in_end]`` will so
        it saves memory.

        :param bytearray out_buffer: buffer containing the bytes to write
        :param bytearray in_buffer: buffer containing the bytes to read into
        :param int out_start: Index to start writing from
        :param int out_end: Index to read up to but not include; if None, use ``len(out_buffer)``
        :param int in_start: Index to start writing at
        :param int in_end: Index to write up to but not include; if None, use ``len(in_buffer)``
        """
        ...

class SPIDevice:
    """SPI Device Manager"""

    def __init__(
        self,
        spi: busio.SPI,
        chip_select: microcontroller.Pin,
        *,
        baudrate: int = 100000,
        polarity: int = 0,
        phase: int = 0,
        extra_clocks: int = 0
    ) -> None:

        """
        Represents a single SPI device and manages locking the bus and the device address.

        :param ~busio.SPI spi: The SPI bus the device is on
        :param ~digitalio.DigitalInOut chip_select: The chip select pin object that implements the DigitalInOut API.
        :param int extra_clocks: The minimum number of clock cycles to cycle the bus after CS is high. (Used for SD cards.)

        Example::

            import busio
            import digitalio
            from board import *
            from adafruit_bus_device.spi_device import SPIDevice
            with busio.SPI(SCK, MOSI, MISO) as spi_bus:
                cs = digitalio.DigitalInOut(D10)
                device = SPIDevice(spi_bus, cs)
                bytes_read = bytearray(4)
                # The object assigned to spi in the with statements below
                # is the original spi_bus object. We are using the busio.SPI
                # operations busio.SPI.readinto() and busio.SPI.write().
                with device as spi:
                    spi.readinto(bytes_read)
                # A second transaction
                with device as spi:
                    spi.write(bytes_read)"""
    ...
    def __enter__(self) -> busio.SPI:
        """Starts a SPI transaction by configuring the SPI and asserting chip select."""
        ...
    def __exit__(self) -> None:
        """Ends a SPI transaction by deasserting chip select. See
        :ref:`lifetime-and-contextmanagers` for more info."""
        ...
