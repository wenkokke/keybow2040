import board
from keybow2040 import Keybow2040

import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

# Set up Keybow
I2C = board.I2C()
KEYBOW = Keybow2040(I2C)

# Set up the keyboard and layout
KEYBOARD = Keyboard(usb_hid.devices)
LAYOUT = KeyboardLayoutUS(KEYBOARD)