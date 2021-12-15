# SPDX-FileCopyrightText: Copyright (c) 2021 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`adafruit_simple_text_display`
================================================================================

A helper library for displaying lines of text on a display using displayio.


* Author(s): Kattni Rembor

Implementation Notes
--------------------

**Hardware:**

Any microcontroller with a built-in display, or an external display.

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases
"""

import board
import displayio
import terminalio
from adafruit_display_text import bitmap_label as label

__version__ = "1.2.1"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_Simple_Text_Display.git"


class SimpleTextDisplay:
    """Easily display lines of text on a display using displayio."""

    # Color variables available for import.
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    ORANGE = (255, 150, 0)
    GREEN = (0, 255, 0)
    TEAL = (0, 255, 120)
    CYAN = (0, 255, 255)
    BLUE = (0, 0, 255)
    PURPLE = (180, 0, 255)
    MAGENTA = (255, 0, 150)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    GOLD = (255, 222, 30)
    PINK = (242, 90, 255)
    AQUA = (50, 255, 255)
    JADE = (0, 255, 40)
    AMBER = (255, 100, 0)
    VIOLET = (255, 0, 255)
    SKY = (0, 180, 255)

    def __init__(
        self,
        title=None,
        title_color=(255, 255, 255),
        title_scale: int = 1,
        title_length: int = 0,  # Ignored - will be removed in a future version
        text_scale: int = 1,
        font=None,
        colors=None,
        display=None,
    ):
        # pylint: disable=too-many-arguments, unused-argument
        """Display lines of text on a display using displayio. Lines of text are created in order as
        shown in the example below. If you skip a number, the line will be shown blank on the
        display, e.g. if you include ``[0]`` and ``[2]``, the second line on the display will be
        empty, and the text specified for lines 0 and 2 will be displayed on the first and third
        line. Remember, Python begins counting at 0, so the first line on the display is 0 in the
        code. Setup occurs before the loop. For data to be dynamically updated on the display, you
        must include the data call in the loop by using ``.text =``. For example, if setup is saved
        as ``temperature_data = simple_text_display()`` then ``temperature_data[0].text =
        microcontroller.cpu.temperature`` must be inside the ``while True:`` loop for the
        temperature data displayed to update as the values change. You must call `show()` at the
        end of the list for anything to display. See example below for usage.

        :param None,str title: The title displayed above the data. Set ``title="Title text"`` to
            provide a title. Defaults to `None`.
        :param None,Tuple(int,int,int) title_color: The color of the title. Not necessary if no
            title is provided. Defaults to white (255, 255, 255).
        :param int title_scale: Scale the size of the title. Not necessary if no title is provided.
            Defaults to 1.
        :param int title_length: DEPRECATED/IGNORED - This will be removed in a future version.
        :param int text_scale: Scale the size of the data lines. Scales the title as well.
            Defaults to 1.
        :param ~fontio.BuiltinFont,~adafruit_bitmap_font.bdf.BDF,~adafruit_bitmap_font.pcf.PCF font:
            The font to use to display the title and data. Defaults to `terminalio.FONT`.
        :param None,Tuple(Tuple(int,int,int),...) colors: A list of colors for the lines of data
            on the display. If you provide a single color, all lines will be that color. Otherwise
            it will cycle through the list you provide if the list is less than the number of lines
            displayed. Default colors are used if ``colors`` is not set. For example, if creating
            two lines of data, ``colors=((255, 255, 255), (255, 0, 0))`` would set the first line
            white and the second line red, and if you created four lines of data with the same
            setup, it would alternate white and red. You can also use the colors built into the
            library. For example, if you import the library as
            ``from adafruit_simple_text_display import SimpleTextDisplay``, you can indicate the
            colors as follows: ``colors=(SimpleTextDisplay.WHITE, SimpleTextDisplay.RED)``.
        :param None,~displayio.Display display: The display object. Defaults to assuming a built-in
            display. To use with an external display, instantiate the display object and provide it
            here. Defaults to ``board.DISPLAY``.

        This example displays two lines with temperature data in C and F on the display.
        Remember to call `show()` after the list to update the display.

        .. code-block:: python

            import microcontroller
            from adafruit_simple_text_display import SimpleTextDisplay

            temperature_data = SimpleTextDisplay(title="Temperature Data!", title_scale=2)

            while True:
                sensor_data[0].text = "Temperature: {:.2f} degrees C".format(
                    microcontroller.cpu.temperature
                )
                sensor_data[1].text = "Temperature: {:.2f} degrees F".format(
                    (microcontroller.cpu.temperature * (9 / 5) + 32)
                )
                sensor_data.show()

        """

        if not colors:
            colors = (
                SimpleTextDisplay.VIOLET,
                SimpleTextDisplay.GREEN,
                SimpleTextDisplay.RED,
                SimpleTextDisplay.CYAN,
                SimpleTextDisplay.ORANGE,
                SimpleTextDisplay.BLUE,
                SimpleTextDisplay.MAGENTA,
                SimpleTextDisplay.SKY,
                SimpleTextDisplay.YELLOW,
                SimpleTextDisplay.PURPLE,
            )

        self._colors = colors
        if display is None:
            display = board.DISPLAY
        self._display = display
        self._font = font if font else terminalio.FONT
        self._text_scale = text_scale

        self.text_group = displayio.Group()

        if title:
            title_label = label.Label(
                self._font,
                text=title,
                color=title_color,
                scale=title_scale,
                anchor_point=(0, 0),
                anchored_position=(0, 0),
            )
            self._next_y = title_label.bounding_box[3] * title_scale

            self.text_group.append(title_label)
        else:
            self._next_y = 0

        self._lines = []
        # Add first line
        self._lines.append(self.add_text_line(color=colors[0]))

    def __getitem__(self, item):
        """Fetch the Nth text line Group"""
        if len(self._lines) - 1 < item:
            for i in range(len(self._lines), item + 1):
                self._lines.append(
                    self.add_text_line(color=self._colors[i % len(self._colors)])
                )
        return self._lines[item]

    def add_text_line(self, color=(255, 255, 255)):
        """Adds a line on the display of the specified color and returns the label object."""

        text_label = label.Label(
            self._font,
            text="Myj",  # Dummy value to allow bounding_box to calculate
            color=color,
            scale=self._text_scale,
            anchor_point=(0, 0),
            anchored_position=(0, self._next_y),
        )
        self._next_y += text_label.bounding_box[3] * text_label.scale
        text_label.text = ""  # Erase the dummy value after using bounding_box
        self.text_group.append(text_label)

        return text_label

    def show(self):
        """Call show() to display the data list."""
        self._display.show(self.text_group)

    def show_terminal(self):
        """Revert to terminalio screen."""
        self._display.show(None)
