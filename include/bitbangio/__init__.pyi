"""Digital protocols implemented by the CPU

The `bitbangio` module contains classes to provide digital bus protocol
support regardless of whether the underlying hardware exists to use the
protocol.

First try to use `busio` module instead which may utilize peripheral
hardware to implement the protocols. Native implementations will be faster
than bitbanged versions and have more capabilities.

All classes change hardware state and should be deinitialized when they
are no longer needed if the program continues after use. To do so, either
call :py:meth:`!deinit` or use a context manager. See
:ref:`lifetime-and-contextmanagers` for more info.

For example::

  import bitbangio
  from board import *

  i2c = bitbangio.I2C(SCL, SDA)
  print(i2c.scan())
  i2c.deinit()

This example will initialize the the device, run
:py:meth:`~bitbangio.I2C.scan` and then :py:meth:`~bitbangio.I2C.deinit` the
hardware. The last step is optional because CircuitPython automatically
resets hardware after a program finishes."""

from __future__ import annotations

from typing import List, Optional

import microcontroller
from _typing import ReadableBuffer, WriteableBuffer

class I2C:
    """Two wire serial protocol"""

    def __init__(
        self,
        scl: microcontroller.Pin,
        sda: microcontroller.Pin,
        *,
        frequency: int = 400000,
        timeout: int = 255
    ) -> None:
        """I2C is a two-wire protocol for communicating between devices.  At the
        physical level it consists of 2 wires: SCL and SDA, the clock and data
        lines respectively.

        .. seealso:: Using this class directly requires careful lock management.
            Instead, use :class:`~adafruit_bus_device.i2c_device.I2CDevice` to
            manage locks.

        .. seealso:: Using this class to directly read registers requires manual
            bit unpacking. Instead, use an existing driver or make one with
            :ref:`Register <register-module-reference>` data descriptors.

        :param ~microcontroller.Pin scl: The clock pin
        :param ~microcontroller.Pin sda: The data pin
        :param int frequency: The clock frequency of the bus
        :param int timeout: The maximum clock stretching timeout in microseconds"""
        ...
    def deinit(self) -> None:
        """Releases control of the underlying hardware so other classes can use it."""
        ...
    def __enter__(self) -> I2C:
        """No-op used in Context Managers."""
        ...
    def __exit__(self) -> None:
        """Automatically deinitializes the hardware on context exit. See
        :ref:`lifetime-and-contextmanagers` for more info."""
        ...
    def scan(self) -> List[int]:
        """Scan all I2C addresses between 0x08 and 0x77 inclusive and return a list of
        those that respond.  A device responds if it pulls the SDA line low after
        its address (including a read bit) is sent on the bus."""
        ...
    def try_lock(self) -> bool:
        """Attempts to grab the I2C lock. Returns True on success."""
        ...
    def unlock(self) -> None:
        """Releases the I2C lock."""
        ...
    def readfrom_into(
        self,
        address: int,
        buffer: WriteableBuffer,
        *,
        start: int = 0,
        end: Optional[int] = None
    ) -> None:
        """Read into ``buffer`` from the device selected by ``address``.
        The number of bytes read will be the length of ``buffer``.
        At least one byte must be read.

        If ``start`` or ``end`` is provided, then the buffer will be sliced
        as if ``buffer[start:end]``. This will not cause an allocation like
        ``buf[start:end]`` will so it saves memory.

        :param int address: 7-bit device address
        :param ~_typing.WriteableBuffer buffer: buffer to write into
        :param int start: Index to start writing at
        :param int end: Index to write up to but not include"""
        ...
    def writeto(
        self,
        address: int,
        buffer: ReadableBuffer,
        *,
        start: int = 0,
        end: Optional[int] = None,
        stop: bool = True
    ) -> None:
        """Write the bytes from ``buffer`` to the device selected by ``address`` and then transmits a
        stop bit. Use `writeto_then_readfrom` when needing a write, no stop and repeated start
        before a read.

        If ``start`` or ``end`` is provided, then the buffer will be sliced
        as if ``buffer[start:end]``. This will not cause an allocation like
        ``buffer[start:end]`` will so it saves memory.

        Writing a buffer or slice of length zero is permitted, as it can be used
        to poll for the existence of a device.

        :param int address: 7-bit device address
        :param ~_typing.ReadableBuffer buffer: buffer containing the bytes to write
        :param int start: Index to start writing from
        :param int end: Index to read up to but not include"""
        ...
    def writeto_then_readfrom(
        self,
        address: int,
        out_buffer: ReadableBuffer,
        in_buffer: ReadableBuffer,
        *,
        out_start: int = 0,
        out_end: Optional[int] = None,
        in_start: int = 0,
        in_end: Optional[int] = None
    ) -> None:
        """Write the bytes from ``out_buffer`` to the device selected by ``address``, generate no stop
        bit, generate a repeated start and read into ``in_buffer``. ``out_buffer`` and
        ``in_buffer`` can be the same buffer because they are used sequentially.

        If ``start`` or ``end`` is provided, then the corresponding buffer will be sliced
        as if ``buffer[start:end]``. This will not cause an allocation like ``buf[start:end]``
        will so it saves memory.

        :param int address: 7-bit device address
        :param ~_typing.ReadableBuffer out_buffer: buffer containing the bytes to write
        :param ~_typing.WriteableBuffer in_buffer: buffer to write into
        :param int out_start: Index to start writing from
        :param int out_end: Index to read up to but not include. Defaults to ``len(buffer)``
        :param int in_start: Index to start writing at
        :param int in_end: Index to write up to but not include. Defaults to ``len(buffer)``"""

class OneWire:
    """Lowest-level of the Maxim OneWire protocol

    :class:`~bitbangio.OneWire` implements the timing-sensitive foundation of
    the Maxim (formerly Dallas Semi) OneWire protocol.

    Protocol definition is here: https://www.maximintegrated.com/en/app-notes/index.mvp/id/126"""

    def __init__(self, pin: microcontroller.Pin) -> None:

        """Create a OneWire object associated with the given pin. The object
        implements the lowest level timing-sensitive bits of the protocol.

        :param ~microcontroller.Pin pin: Pin to read pulses from.

        Read a short series of pulses::

          import bitbangio
          import board

          onewire = bitbangio.OneWire(board.D7)
          onewire.reset()
          onewire.write_bit(True)
          onewire.write_bit(False)
          print(onewire.read_bit())"""
        ...
    def deinit(self) -> None:
        """Deinitialize the OneWire bus and release any hardware resources for reuse."""
        ...
    def __enter__(self) -> OneWire:
        """No-op used by Context Managers."""
        ...
    def __exit__(self) -> None:
        """Automatically deinitializes the hardware when exiting a context. See
        :ref:`lifetime-and-contextmanagers` for more info."""
        ...
    def reset(self) -> bool:
        """Reset the OneWire bus"""
        ...
    def read_bit(self) -> bool:
        """Read in a bit

        :returns: bit state read
        :rtype: bool"""
        ...
    def write_bit(self, value: bool) -> None:
        """Write out a bit based on value."""
        ...

class SPI:
    """A 3-4 wire serial protocol

    SPI is a serial protocol that has exclusive pins for data in and out of the
    main device.  It is typically faster than :py:class:`~bitbangio.I2C` because a
    separate pin is used to select a device rather than a transmitted
    address. This class only manages three of the four SPI lines: `!clock`,
    `!MOSI`, `!MISO`. Its up to the client to manage the appropriate
    select line, often abbreviated `!CS` or `!SS`. (This is common because
    multiple secondaries can share the `!clock`, `!MOSI` and `!MISO` lines
    and therefore the hardware.)"""

    def __init__(
        self,
        clock: microcontroller.Pin,
        MOSI: Optional[microcontroller.Pin] = None,
        MISO: Optional[microcontroller.Pin] = None,
    ) -> None:
        """Construct an SPI object on the given pins.

        .. seealso:: Using this class directly requires careful lock management.
            Instead, use :class:`~adafruit_bus_device.spi_device.SPIDevice` to
            manage locks.

        .. seealso:: Using this class to directly read registers requires manual
            bit unpacking. Instead, use an existing driver or make one with
            :ref:`Register <register-module-reference>` data descriptors.


        :param ~microcontroller.Pin clock: the pin to use for the clock.
        :param ~microcontroller.Pin MOSI: the Main Out Selected In pin.
        :param ~microcontroller.Pin MISO: the Main In Selected Out pin."""
        ...
    def deinit(self) -> None:
        """Turn off the SPI bus."""
        ...
    def __enter__(self) -> SPI:
        """No-op used by Context Managers."""
        ...
    def __exit__(self) -> None:
        """Automatically deinitializes the hardware when exiting a context. See
        :ref:`lifetime-and-contextmanagers` for more info."""
        ...
    def configure(
        self,
        *,
        baudrate: int = 100000,
        polarity: int = 0,
        phase: int = 0,
        bits: int = 8
    ) -> None:
        """Configures the SPI bus. Only valid when locked.

        :param int baudrate: the clock rate in Hertz
        :param int polarity: the base state of the clock line (0 or 1)
        :param int phase: the edge of the clock that data is captured. First (0)
          or second (1). Rising or falling depends on clock polarity.
        :param int bits: the number of bits per word"""
        ...
    def try_lock(self) -> bool:
        """Attempts to grab the SPI lock. Returns True on success.

        :return: True when lock has been grabbed
        :rtype: bool"""
        ...
    def unlock(self) -> None:
        """Releases the SPI lock."""
        ...
    def write(self, buf: ReadableBuffer) -> None:
        """Write the data contained in ``buf``. Requires the SPI being locked.
        If the buffer is empty, nothing happens."""
        ...
    def readinto(
        self,
        buffer: WriteableBuffer,
        *,
        start: int = 0,
        end: Optional[int] = None,
        write_value: int = 0
    ) -> None:
        """Read into ``buffer`` while writing ``write_value`` for each byte read.
        The SPI object must be locked.
        If the number of bytes to read is 0, nothing happens.

        :param bytearray buffer: Read data into this buffer
        :param int start: Start of the slice of ``buffer`` to read into: ``buffer[start:end]``
        :param int end: End of the slice; this index is not included. Defaults to ``len(buffer)``
        :param int write_value: Value to write while reading."""
        ...
    def write_readinto(
        self,
        buffer_out: ReadableBuffer,
        buffer_in: ReadableBuffer,
        *,
        out_start: int = 0,
        out_end: Optional[int] = None,
        in_start: int = 0,
        in_end: Optional[int] = None
    ) -> None:
        """Write out the data in ``buffer_out`` while simultaneously reading data into ``buffer_in``.
        The SPI object must be locked.
        The lengths of the slices defined by ``buffer_out[out_start:out_end]`` and ``buffer_in[in_start:in_end]``
        must be equal.
        If buffer slice lengths are both 0, nothing happens.

        :param ~_typing.ReadableBuffer buffer_out: Write out the data in this buffer
        :param ~_typing.WriteableBuffer buffer_in: Read data into this buffer
        :param int out_start: Start of the slice of buffer_out to write out: ``buffer_out[out_start:out_end]``
        :param int out_end: End of the slice; this index is not included. Defaults to ``len(buffer_out)``
        :param int in_start: Start of the slice of ``buffer_in`` to read into: ``buffer_in[in_start:in_end]``
        :param int in_end: End of the slice; this index is not included. Defaults to ``len(buffer_in)``"""
        ...
