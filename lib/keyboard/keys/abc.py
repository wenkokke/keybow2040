from keybow2040 import Key


class KeyAction:

    def hook(self, key: Key):
        """Hook the action to a key."""
        if key:
            key.press_function = self.on_press
            key.release_function = self.on_release
            key.hold_function = self.on_hold

    def update(self, key: Key):
        """Called every cycle."""

    def on_press(self, key: Key):
        """Called when the key is pressed."""

    def on_release(self, key: Key):
        """Called when the key is released."""

    def on_hold(self, key: Key):
        """Called when the key is held."""


class And(KeyAction):
    def __init__(self, first: KeyAction, second: KeyAction) -> None:
        super().__init__()
        self.first = first
        self.second = second

    def update(self, key: Key):
        """Called every cycle."""
        self.first.update(key)
        self.second.update(key)

    def on_press(self, key: Key):
        """Called when the key is pressed."""
        self.first.on_press(key)
        self.second.on_press(key)

    def on_release(self, key: Key):
        """Called when the key is released."""
        self.first.on_release(key)
        self.second.on_release(key)

    def on_hold(self, key: Key):
        """Called when the key is held."""
        self.first.on_hold(key)
        self.second.on_hold(key)
