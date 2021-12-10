from keyboard import globals
from keybow2040 import number_to_xy

class Layer:
    def __init__(self, key_action_matrix, reverse=True):
        if reverse:
            self.key_action_matrix = tuple(reversed(key_action_matrix))
        else:
            self.key_action_matrix = key_action_matrix

    def hook(self):
        for key in globals.KEYBOW.keys:
            x, y = number_to_xy(key.number)
            self.key_action_matrix[x][y].hook(key)

    def update(self):
        for key in globals.KEYBOW.keys:
            x, y = number_to_xy(key.number)
            self.key_action_matrix[x][y].update(key)
