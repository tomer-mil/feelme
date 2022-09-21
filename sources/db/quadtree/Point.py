import numpy as np
from items.Song import Song


class Point:
    """
    A Point item represents a point in a 2D space by (x,y).
    Each Point has a payload of a Song object.
    """

    def __init__(self, x: float = 0.00, y: float = 0.00, payload: Song = None):
        self.x, self.y = x, y
        self.payload = payload

    def __repr__(self):
        return f"({self.x}, {self.y}) | {repr(self.payload)}"

    def __str__(self):
        return self.__repr__()

    def distance_to(self, other):
        try:
            other_x, other_y = other.x, other.y
        except AttributeError:
            raise AttributeError(f"Can't measure distance between Point and {type(other)}")

        return np.hypot(self.x - other_x, self.y - other_y)

