
from keybow2040 import number_to_xy

class Layer:
    def __init__(self, *action_matrix, reverse=True):
        if reverse:
            self.action_matrix = tuple(reversed(action_matrix))
        else:
            self.action_matrix = action_matrix

    def press(self, key):
        x, y = number_to_xy(key.number)
        self.action_matrix[x][y].on_press()
