from keyboard import globals
from keyboard.keys.abc import KeyAction
from adafruit_hid.keycode import Keycode # type: ignore
from keybow2040 import Key

class Press(KeyAction):
    """Press a series of keys based on a string.
    """

    SpecialKeys = {
        'alt': Keycode.ALT,
        'cmd': Keycode.COMMAND,
        'ctrl': Keycode.CONTROL,
        'option': Keycode.OPTION,
        'shift': Keycode.SHIFT,
        'space': Keycode.SPACE,
        'tab': Keycode.TAB,
        'left': Keycode.LEFT_ARROW,
        'right': Keycode.RIGHT_ARROW,
        'up': Keycode.UP_ARROW,
        'down': Keycode.DOWN_ARROW,
    }

    @staticmethod
    def parse_chords(chords: str):
        keycodes_chords = []
        for chord in chords.split(' '):
            keycodes_chord = []
            for keyname in chord.split('-'):
                try:
                    keycodes_chord.append(Press.SpecialKeys[keyname])
                except KeyError:
                    keycodes_chord.extend(globals.LAYOUT.keycodes(keyname))
            keycodes_chords.append(keycodes_chord)
        return keycodes_chords

    def __init__(self, chords: str) -> None:
        super().__init__()
        self.keycodes_chords = Press.parse_chords(chords)

    def on_press(self, key: Key):
        for keycodes_chord in self.keycodes_chords:
            globals.KEYBOARD.send(*keycodes_chord)

