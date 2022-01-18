
from typing import Tuple


class Point3D:
    """Vector three dimensional

    Attributes:
        x (float): X axis
        y (float): Y axis
        z (float): Z axis
    """

    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        """Creates a Point3D (three-dimensional vector)

        Args:
            x (float): X axis
            y (float): Y axis
            z (float): Z axis
        """

        self.x = x
        self.y = y
        self.z = z

    @classmethod
    def from_tuple(cls, tuple: Tuple[float, float, float]):
        """Creates a Point3D from a tuple"""

        if tuple is None:
            return cls()

        return cls(tuple[0], tuple[1], tuple[2])


