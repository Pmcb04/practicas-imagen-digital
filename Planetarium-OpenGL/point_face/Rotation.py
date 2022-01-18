from typing import Tuple


class Rotation:
    """Rotation in Euler angles

    Attributes:
        alpha (float): Rotation around the Z axis
        beta (float): Rotation around the X axis
        gamma (float): Rotation around the Y axis
    """

    def __init__(self, alpha: float = 0, beta: float = 0, gamma: float = 0):
        """Creates a Rotation

        Args:
            alpha (float): Rotation around the Z axis
            beta (float): Rotation around the X axis
            gamma (float): Rotation around the Y axis
        """

        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

    @classmethod
    def from_tuple(cls, tuple: Tuple[float, float, float]):
        """Creates a Rotation from a tuple"""

        if tuple is None:
            return cls()

        return cls(tuple[0], tuple[1], tuple[2])


