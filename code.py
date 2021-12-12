# SPDX-FileCopyrightText: 2021 Sandy Macdonald
#
# SPDX-License-Identifier: MIT

# A simple example of how to set up a keymap and HID keyboard on Keybow 2040.

# You'll need to connect Keybow 2040 to a computer, as you would with a regular
# USB keyboard.

# Drop the keybow2040.py file into your `lib` folder on your `CIRCUITPY` drive.

# NOTE! Requires the adafruit_hid CircuitPython library also!

from adafruit_hid.keyboard import Keyboard # type: ignore
from keyboard import globals
from keyboard.keys.abc import *
from keyboard.keys.press import *
from keyboard.keys import light
from keyboard.layers import *

# The colour to set the keys when pressed.
WHITE = (255, 252, 254)
PURPLE = (36, 30, 47)
PINK = (255, 152, 186)
LAVENDER = (230, 230, 250)
INDIGO = (148, 87, 235)
TALON = (38, 82, 111)
ZOOMUS = (45, 140, 255)

ShortCat = And(light.SwitchWhenPressed(PURPLE, PINK), Press('ctrl-alt-cmd-C'))
ToggleTalon = And(light.Mirror(Keyboard.LED_CAPS_LOCK, PURPLE, PINK), Press('cmd-ctrl-alt-T'))
ToggleMuted = And(light.Mirror(Keyboard.LED_NUM_LOCK, PURPLE, PINK), Press('cmd-ctrl-alt-Z'))
Disabled = light.AlwaysOn(PURPLE)

layer1 = Layer([
    [Disabled, Disabled,    Disabled,    Disabled],
    [Disabled, Disabled,    Disabled,    Disabled],
    [Disabled, Disabled,    Disabled,    Disabled],
    [Disabled, ToggleTalon, ToggleMuted, ShortCat],
])

layer1.hook()

while True:
    # Always remember to call KEYBOW.update()!
    globals.KEYBOW.update()
    layer1.update()
