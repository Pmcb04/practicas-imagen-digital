from OpenGL.raw.GL.VERSION.GL_1_0 import *


class Spotlight: 

    def __init__(self, id=None, diffused_light=None, ambient_light=None, specular_light=None, position=None):
        self.id = id
        self.diffused_light = diffused_light
        self.ambient_light = ambient_light
        self.specular_light = specular_light
        self.position = position

    def on(self):
        glLightfv(GL_LIGHT0+self.id, GL_DIFFUSE, self.diffused_light)
        glLightfv(GL_LIGHT0+self.id, GL_AMBIENT, self.ambient_light)
        glLightfv(GL_LIGHT0+self.id, GL_SPECULAR, self.specular_light)
        glLightfv(GL_LIGHT0+self.id, GL_POSITION, self.position)

        glEnable(GL_LIGHT0 + self.id)

    def off(self):
        glDisable(GL_LIGHT0 + self.id)

    def __str__(self):
        return ''' 
        [SPOTLIGHT]
        id -> {}
        diffused_light -> {}
        ambient_light -> {}
        specular_light -> {}
        location -> {}
        '''.format(self.id, self.diffused_light, self.ambient_light, self.specular_light, self.position)