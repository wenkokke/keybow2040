# SPDX-FileCopyrightText: 2021 Sandy Macdonald
#
# SPDX-License-Identifier: MIT

# A simple example of how to set up a keymap and HID keyboard on Keybow 2040.

# You'll need to connect Keybow 2040 to a computer, as you would with a regular
# USB keyboard.

# Drop the keybow2040.py file into your `lib` folder on your `CIRCUITPY` drive.

# NOTE! Requires the adafruit_hid CircuitPython library also!

from keyboard import globals
from keyboard.keys.disable import Disabled
from keyboard.keys.press import *
from keyboard.layers import *

ToggleTalon = Press('ctrl-alt-M')
ToggleMuted = Press('ctrl-alt-cmd-M')

layer1 = Layer(
    [Disabled, ToggleTalon, ToggleMuted, Disabled],
    [Disabled, Disabled,    Disabled,    Disabled],
    [Disabled, Disabled,    Disabled,    Disabled],
    [Disabled, Disabled,    Disabled,    Disabled])


# The colour to set the keys when pressed.
WHITE = (255, 252, 254)
PURPLE = (36, 30, 47)
PINK = (255, 152, 186)
LAVENDER = (230, 230, 250)
INDIGO = (148, 87, 235)

# Attach handler functions to all of the keys
for key in globals.KEYBOW.keys:
    # A press handler that sends the keycode and turns on the LED
    @globals.KEYBOW.on_press(key)
    def press_handler(key):
        layer1.press(key)
        key.set_led(*LAVENDER)

    # A release handler that turns off the LED
    @globals.KEYBOW.on_release(key)
    def release_handler(key):
        key.led_off()

while True:
    # Always remember to call KEYBOW.update()!
    globals.KEYBOW.update()
