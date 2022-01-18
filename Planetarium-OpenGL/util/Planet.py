from OpenGL.raw.GL.VERSION.GL_1_0 import *
from OpenGL.raw.GL.VERSION.GL_1_1 import *
from OpenGL.raw.GL.VERSION.GL_4_5 import *
from util.Modelo import Modelo 
import math
from PIL import Image

class Planet(Modelo):

    def __init__(self, inclination=None, radius=None, name=None, wRotAstro=None, wRotProp=None, size=None, moons=None, material=None):
        self.inclination = inclination
        self.radius = radius
        self.name = name
        self.wRotAstro = wRotAstro
        self.wRotProp = wRotProp
        self.size = size
        self.moons = moons
        self.material = material

    def rotate(self, t):
        glRotatef(self.inclination, 0 , self.wRotProp * t, 0) # rotacion del astro con su propio eje

    def translate(self, t, zoom):
        glTranslatef(
            self.radius * zoom / 100 * math.cos(self.wRotAstro * t * math.pi / 360), 
            0,
            self.radius * zoom / 100 * math.sin(self.wRotAstro * t * math.pi / 360)
        )

    def __str__(self, type):
        return ''' 
        [{}]
        name -> {}
        wRotAstro -> {}
        wRotProp -> {}
        size -> {}
        material -> {}
        '''.format(type,self.name, self.wRotAstro, self.wRotProp, self.size, self.material.__str__())