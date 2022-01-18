from typing import Tuple
from point_face.Point3D import Point3D
from util.TNormal import TNormal

class Face:
    """Face of a 3D model, a triangle made up of 3 points

    Attributes:
        a (int): The index in the vertices list for the vertex A
        b (int): The index in the vertices list for the vertex B
        c (int): The index in the vertices list for the vertex C
        normal (TNormal): The Normal vector of the Face
    """

    def __init__(self, a: int, b: int, c: int, normal: TNormal):
        """Creates a Face

        Args:
            a (int): Reference to vertex A in the vertices list
            b (int): Reference to vertex B in the vertices list
            c (int): Reference to vertex C in the vertices list
            normal (TNormal): The Normal vector of the Face
        """

        self.a = a
        self.b = b
        self.c = c
        self.normal = normal

    @classmethod
    def from_tuple(cls, tuple: Tuple[int, int, int, Point3D]):
        """Creates a Face from a tuple"""

        if tuple is None:
            return cls()

        return cls(tuple[0], tuple[1], tuple[2], tuple[3])

    def getA(self):
        return self.a
    
    def setA(self,a):
        self.a=a

    def getB(self):
        return self.b
    
    def setB(self,b):
        self.b=b

    def getC(self):
        return self.c
    
    def setC(self,c):
        self.c=c

    def getNormal(self):
        return self.normal
    
    def setNormal(self,normal):
        self.normal=normal


