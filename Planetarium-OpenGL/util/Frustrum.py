
from OpenGL.raw.GL.VERSION.GL_1_0 import *
from OpenGL.raw.GLU import gluPerspective


class Frustum:

    def __init__(self, alpha , aspect, near, far):
        
        self.alpha = alpha
        self.aspect = aspect
        self.near = near
        self.far = far

    def set(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity() # Apilamos la vista
        gluPerspective(self.alpha, self.aspect, self.near, self.far)

    def __str__(self):
        return ''' 
        [FRUSTUM]
        alpha -> {}
        aspect -> {}
        near -> {}
        far -> {}
        '''.format(
            self.alpha, 
            self.aspect, 
            self.near, 
            self.far)

    