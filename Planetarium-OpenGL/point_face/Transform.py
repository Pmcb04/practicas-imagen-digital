from point_face import Point3D
from point_face import Rotation


class Transform:
    """Transform holds position, scaling and rotation for an object in the World

    Attributes:
        position (Point3D): Position in the 3D World
        scaling (Point3D): Scaling of the Object
        rotation (Rotation): Rotation of the Object
    """

    def __init__(self, position: Point3D = Point3D(), scaling: Point3D = Point3D(), rotation: Rotation = Rotation()):
        """Creates a Transform data

        Args:
            position (Point3D): Position in the 3D World
            scaling (Point3D): Scaling of the Object
            rotation (Rotation): Rotation of the Object
        """

        self.position = position
        self.scaling = scaling
        self.rotation = rotation
