from OpenGL.raw.GLU import gluLookAt, gluPerspective
from OpenGL.raw.GL.VERSION.GL_1_0 import *

class Camera: 

    def __init__(self, x_axis, y_axis, z_axis, center_x, center_y, center_z, up_x, up_y, up_z):

            self.x_axis=x_axis
            self.y_axis=y_axis
            self.z_axis=z_axis
            self.center_x=center_x
            self.center_y=center_y
            self.center_z=center_z
            self.up_x=up_x
            self.up_y=up_y
            self.up_z=up_z

    def on(self):
        self.frustum.set()
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity() # Apilamos la vista
        gluLookAt(self.x_axis, self.y_axis, self.z_axis, self.center_x, self.center_y, self.center_z, self.up_x, self.up_y, self.up_z)
    
    def setFrustum(self, frustum):
        self.frustum = frustum
        
    def __str__(self):
        return ''' 
        [CAMERA]
        x_axis -> {}
        y_axis -> {}
        z_axis -> {}
        center_x -> {}
        center_y -> {}
        center_z -> {}
        up_x -> {}
        up_y -> {}
        up_z -> {}
        '''.format(
            self.x_axis, 
            self.y_axis, 
            self.z_axis, 
            self.center_x, 
            self.center_y, 
            self.center_z,
            self.up_x, 
            self.up_y,
            self.up_z,
            print(self.frustum.__str__()))