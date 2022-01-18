
from typing import Tuple

class Point2D:
    """Vector two dimensional

    Attributes:
        x (float): X axis
        y (float): Y axis
    """

    def __init__(self, x: float = 0, y: float = 0):
        """Creates a Point2D (two-dimensional vector)

        Args:
            x (float): X axis
            y (float): Y axis
        """

        self.x = x
        self.y = y

    @classmethod
    def from_tuple(cls, tuple: Tuple[float, float]):
        """Creates a Point2D from a tuple"""

        if tuple is None:
            return cls()

        return cls(tuple[0], tuple[1])


