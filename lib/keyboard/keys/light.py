from keyboard import globals
from keyboard.keys.abc import KeyAction
from keybow2040 import Key


class Light(KeyAction):

    def __init__(self, color) -> None:
        super().__init__()
        self.color = color

    def update(self, key: Key):
        key.set_led(*self.color)


class Toggle(Light):
    def __init__(self, color_off, color_on) -> None:
        super().__init__(color_off)
        self.onoff = False
        self.COLOR_OFF = color_off
        self.COLOR_ON = color_on

    def on_press(self, key: Key):
        self.onoff = not self.onoff
        self.color = self.COLOR_ON if self.onoff else self.COLOR_OFF


class Mirror(KeyAction):
    def __init__(self, led: int, color_off, color_on) -> None:
        super().__init__()
        self.LED = led
        self.COLOR_OFF = color_off
        self.COLOR_ON = color_on

    def update(self, key: Key):
        if globals.KEYBOARD.led_on(self.LED):
            key.set_led(*self.COLOR_ON)
        else:
            key.set_led(*self.COLOR_OFF)
