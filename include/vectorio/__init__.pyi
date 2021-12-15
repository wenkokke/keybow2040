"""Lightweight 2d shapes for displays"""

from __future__ import annotations

from typing import List, Tuple, Union

import displayio

class Circle:
    def __init__(
        self,
        pixel_shader: Union[displayio.ColorConverter, displayio.Palette],
        radius: int,
        x: int,
        y: int,
    ) -> None:
        """Circle is positioned on screen by its center point.

        :param pixel_shader: The pixel shader that produces colors from values
        :param radius: The radius of the circle in pixels
        :param x: Initial x position of the axis.
        :param y: Initial y position of the axis."""
    radius: int
    """The radius of the circle in pixels."""

class Polygon:
    def __init__(
        self,
        pixel_shader: Union[displayio.ColorConverter, displayio.Palette],
        points: List[Tuple[int, int]],
        x: int,
        y: int,
    ) -> None:
        """Represents a closed shape by ordered vertices

        :param pixel_shader: The pixel shader that produces colors from values
        :param points: Vertices for the polygon
        :param x: Initial screen x position of the 0,0 origin in the points list.
        :param y: Initial screen y position of the 0,0 origin in the points list."""
    points: List[Tuple[int, int]]
    """Set a new look and shape for this polygon"""

class Rectangle:
    def __init__(
        self,
        pixel_shader: Union[displayio.ColorConverter, displayio.Palette],
        width: int,
        height: int,
        x: int,
        y: int,
    ) -> None:
        """Represents a rectangle by defining its bounds

        :param pixel_shader: The pixel shader that produces colors from values
        :param width: The number of pixels wide
        :param height: The number of pixels high
        :param x: Initial x position of the top left corner.
        :param y: Initial y position of the top left corner."""
