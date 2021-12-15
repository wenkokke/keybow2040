# SPDX-FileCopyrightText: 2019 Brent Rubell for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_cursorcontrol.cursorcontrol_cursormanager`
================================================================================
Simple interaction user interface interaction for Adafruit_CursorControl.
* Author(s): Brent Rubell
"""
import board
from micropython import const
import analogio
from keypad import ShiftRegisterKeys, Event
from adafruit_debouncer import Debouncer

__version__ = "2.5.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_CursorControl.git"


# PyBadge
PYBADGE_BUTTON_LEFT = const(7)
PYBADGE_BUTTON_UP = const(6)
PYBADGE_BUTTON_DOWN = const(5)
PYBADGE_BUTTON_RIGHT = const(4)
# PyBadge & PyGamer
PYBADGE_BUTTON_A = const(1)


class CursorManager:
    """Simple interaction user interface interaction for Adafruit_CursorControl.

    :param adafruit_cursorcontrol cursor: The cursor object we are using.
    """

    def __init__(self, cursor):
        self._cursor = cursor
        self._is_clicked = False
        self._pad_states = 0
        self._event = Event()
        self._init_hardware()

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.deinit()

    def deinit(self):
        """Deinitializes a CursorManager object."""
        self._is_deinited()
        self._pad.deinit()
        self._cursor.deinit()
        self._cursor = None
        self._event = None

    def _is_deinited(self):
        """Checks if CursorManager object has been deinitd."""
        if self._cursor is None:
            raise ValueError(
                "CursorManager object has been deinitialized and can no longer "
                "be used. Create a new CursorManager object."
            )

    def _init_hardware(self):
        """Initializes PyBadge or PyGamer hardware."""
        if hasattr(board, "BUTTON_CLOCK") and not hasattr(board, "JOYSTICK_X"):
            self._pad_btns = {
                "btn_left": PYBADGE_BUTTON_LEFT,
                "btn_right": PYBADGE_BUTTON_RIGHT,
                "btn_up": PYBADGE_BUTTON_UP,
                "btn_down": PYBADGE_BUTTON_DOWN,
                "btn_a": PYBADGE_BUTTON_A,
            }
            self._pad_states = 0
        elif hasattr(board, "JOYSTICK_X"):
            self._joystick_x = analogio.AnalogIn(board.JOYSTICK_X)
            self._joystick_y = analogio.AnalogIn(board.JOYSTICK_Y)
            self._pad_btns = {"btn_a": PYBADGE_BUTTON_A}
            # Sample the center points of the joystick
            self._center_x = self._joystick_x.value
            self._center_y = self._joystick_y.value
        else:
            raise AttributeError(
                "Board must have a D-Pad or Joystick for use with CursorManager!"
            )
        self._pad = ShiftRegisterKeys(
            clock=board.BUTTON_CLOCK,
            data=board.BUTTON_OUT,
            latch=board.BUTTON_LATCH,
            key_count=8,
            value_when_pressed=True,
        )

    @property
    def is_clicked(self):
        """Returns True if the cursor button was pressed
        during previous call to update()
        """
        return self._is_clicked

    def update(self):
        """Updates the cursor object."""
        if self._pad.events.get_into(self._event):
            self._store_button_states()
        self._check_cursor_movement()
        if self._is_clicked:
            self._is_clicked = False
        elif self._pad_states & (1 << self._pad_btns["btn_a"]):
            self._is_clicked = True

    def _read_joystick_x(self, samples=3):
        """Read the X analog joystick on the PyGamer.
        :param int samples: How many samples to read and average.
        """
        reading = 0
        # pylint: disable=unused-variable
        if hasattr(board, "JOYSTICK_X"):
            for _ in range(0, samples):
                reading += self._joystick_x.value
            reading /= samples
        return reading

    def _read_joystick_y(self, samples=3):
        """Read the Y analog joystick on the PyGamer.
        :param int samples: How many samples to read and average.
        """
        reading = 0
        # pylint: disable=unused-variable
        if hasattr(board, "JOYSTICK_Y"):
            for _ in range(0, samples):
                reading += self._joystick_y.value
            reading /= samples
        return reading

    def _store_button_states(self):
        """Stores the state of the PyBadge's D-Pad or the PyGamer's Joystick
        into a byte

        :param Event event: The latest button press transition event detected.
        """
        bit_index = self._event.key_number
        current_state = (self._pad_states >> bit_index) & 1
        if current_state != self._event.pressed:
            self._pad_states = (1 << bit_index) ^ self._pad_states

    def _check_cursor_movement(self):
        """Checks the PyBadge D-Pad or the PyGamer's Joystick for movement."""
        if hasattr(board, "BUTTON_CLOCK") and not hasattr(board, "JOYSTICK_X"):
            if self._pad_states & (1 << self._pad_btns["btn_right"]):
                self._cursor.x += self._cursor.speed
            elif self._pad_states & (1 << self._pad_btns["btn_left"]):
                self._cursor.x -= self._cursor.speed

            if self._pad_states & (1 << self._pad_btns["btn_up"]):
                self._cursor.y -= self._cursor.speed
            elif self._pad_states & (1 << self._pad_btns["btn_down"]):
                self._cursor.y += self._cursor.speed
        elif hasattr(board, "JOYSTICK_X"):
            joy_x = self._read_joystick_x()
            joy_y = self._read_joystick_y()
            if joy_x > self._center_x + 1000:
                self._cursor.x += self._cursor.speed
            elif joy_x < self._center_x - 1000:
                self._cursor.x -= self._cursor.speed
            if joy_y > self._center_y + 1000:
                self._cursor.y += self._cursor.speed
            elif joy_y < self._center_y - 1000:
                self._cursor.y -= self._cursor.speed
        else:
            raise AttributeError(
                "Board must have a D-Pad or Joystick for use with CursorManager!"
            )


class DebouncedCursorManager(CursorManager):
    """Simple interaction user interface interaction for Adafruit_CursorControl.
    This subclass provide a debounced version on the A button and provides queries for when
    the button is just pressed, and just released, as well it's current state. "Just" in this
    context means "since the previous call to update."

    :param adafruit_cursorcontrol cursor: The cursor object we are using.
    """

    def __init__(self, cursor, debounce_interval=0.01):
        CursorManager.__init__(self, cursor)
        self._debouncer = Debouncer(
            lambda: bool(self._pad_states & (1 << self._pad_btns["btn_a"])),
            interval=debounce_interval,
        )

    @property
    def is_clicked(self):
        """Returns True if the cursor button was pressed
        during previous call to update()
        """
        return self._debouncer.rose

    pressed = is_clicked

    @property
    def released(self):
        """Returns True if the cursor button was released
        during previous call to update()
        """
        return self._debouncer.fell

    @property
    def held(self):
        """Returns True if the cursor button is currently being held"""
        return self._debouncer.value

    def update(self):
        """Updates the cursor object."""
        if self._pad.events.get_into(self._event):
            self._store_button_states()
        self._check_cursor_movement()
        self._debouncer.update()
