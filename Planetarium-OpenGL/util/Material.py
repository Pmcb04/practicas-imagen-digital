from OpenGL.raw.GL.VERSION.GL_1_0 import *


class Material:

    def __init__(self, shine=None, diffused_light=None, ambient_light=None, specular_light=None,):
        self.shine = shine
        self.diffused_light = diffused_light
        self.ambient_light = ambient_light
        self.specular_light = specular_light

    def start(self):
        glMaterialf(GL_FRONT, GL_SHININESS, self.shine)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, self.diffused_light)
        glMaterialfv(GL_FRONT, GL_AMBIENT, self.ambient_light)
        glMaterialfv(GL_FRONT, GL_SPECULAR, self.specular_light)

    def __str__(self):
        return ''' 
        [MATERIAL]
        shine -> {}
        diffused_light -> {}
        ambient_light -> {}
        specular_light -> {}
        '''.format(self.shine, self.diffused_light, self.ambient_light, self.specular_light)