"""Support for "Parallel capture" interfaces"""

from __future__ import annotations

from typing import List, Optional

import microcontroller
from _typing import WriteableBuffer

class ParallelImageCapture:
    """Capture image frames from a camera with parallel data interface"""

    def __init__(
        self,
        *,
        data_pins: List[microcontroller.Pin],
        clock: microcontroller.Pin,
        vsync: Optional[microcontroller.Pin],
        href: Optional[microcontroller.Pin],
    ) -> None:
        """Create a parallel image capture object

        :param List[microcontroller.Pin] data_pins: The data pins.
        :param microcontroller.Pin clock: The pixel clock input.
        :param microcontroller.Pin vsync: The vertical sync input, which has a negative-going pulse at the beginning of each frame.
        :param microcontroller.Pin href: The horizontal reference input, which is high whenever the camera is transmitting valid pixel information.
        """
        ...
    def capture(
        self, buffer: WriteableBuffer, width: int, height: int, bpp: int = 16
    ) -> None:
        """Capture a single frame into the given buffer"""
        ...
    def deinit(self) -> None:
        """Deinitialize this instance"""
        ...
    def __enter__(self) -> ParallelImageCapture:
        """No-op used in Context Managers."""
        ...
    def __exit__(self) -> None:
        """Automatically deinitializes the hardware on context exit. See
        :ref:`lifetime-and-contextmanagers` for more info."""
        ...
