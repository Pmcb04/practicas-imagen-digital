from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from OpenGL import *

class Modelo:  

    points3DList=[]
    facesList=[]

    def __init__(self, numCaras=None, numVertices=None):
        self.beta=0
        self.alpha=0
        self.numCaras = numCaras
        self.numVertices = numVertices   

    def drawWired(self, scale_from_editor, zoom):
        for face in self.facesList:
            glDisable(GL_LIGHTING)
            glBegin(GL_LINES) 

            glVertex3f(self.points3DList[face.a].x * scale_from_editor * zoom, self.points3DList[face.a].y * scale_from_editor * zoom, self.points3DList[face.a].z * scale_from_editor * zoom)
            glVertex3f(self.points3DList[face.b].x * scale_from_editor * zoom, self.points3DList[face.b].y * scale_from_editor * zoom, self.points3DList[face.b].z * scale_from_editor * zoom)
            glVertex3f(self.points3DList[face.c].x * scale_from_editor * zoom, self.points3DList[face.c].y * scale_from_editor * zoom, self.points3DList[face.c].z * scale_from_editor * zoom)
            glVertex3f(self.points3DList[face.a].x * scale_from_editor * zoom, self.points3DList[face.a].y * scale_from_editor * zoom, self.points3DList[face.a].z * scale_from_editor * zoom)

        
            glEnd()

    def drawSolid(self, scale_from_editor, zoom):
        for face in self.facesList:
            glEnable(GL_LIGHTING)
            glBegin(GL_POLYGON)
            
            glVertex3f(self.points3DList[face.a].x * scale_from_editor * zoom, self.points3DList[face.a].y * scale_from_editor * zoom, self.points3DList[face.a].z * scale_from_editor * zoom)
            glVertex3f(self.points3DList[face.b].x * scale_from_editor * zoom, self.points3DList[face.b].y * scale_from_editor * zoom, self.points3DList[face.b].z * scale_from_editor * zoom)
            glVertex3f(self.points3DList[face.c].x * scale_from_editor * zoom, self.points3DList[face.c].y * scale_from_editor * zoom, self.points3DList[face.c].z * scale_from_editor * zoom)
            
            glEnd()

    def drawFlat(self, scale_from_editor, zoom):
        for face in self.facesList:
            glShadeModel(GL_FLAT)
            glEnable(GL_LIGHTING)
            glBegin(GL_POLYGON)

            glNormal3f(self.points3DList[face.a].x * scale_from_editor * zoom, self.points3DList[face.a].y * scale_from_editor * zoom, self.points3DList[face.a].z * scale_from_editor * zoom)

            glVertex3f(self.points3DList[face.a].x * scale_from_editor * zoom, self.points3DList[face.a].y * scale_from_editor * zoom, self.points3DList[face.a].z * scale_from_editor * zoom)
            glVertex3f(self.points3DList[face.b].x * scale_from_editor * zoom, self.points3DList[face.b].y * scale_from_editor * zoom, self.points3DList[face.b].z * scale_from_editor * zoom)
            glVertex3f(self.points3DList[face.c].x * scale_from_editor * zoom, self.points3DList[face.c].y * scale_from_editor * zoom, self.points3DList[face.c].z * scale_from_editor * zoom)
        
            glEnd()

    def drawSmooth(self, scale_from_editor, zoom):
        for face in self.facesList:
            glShadeModel(GL_SMOOTH)
            glEnable(GL_LIGHTING)
            glBegin(GL_POLYGON)

            glNormal3f(self.points3DList[face.a].x * scale_from_editor * zoom, self.points3DList[face.a].y * scale_from_editor * zoom, self.points3DList[face.a].z * scale_from_editor * zoom)
            glVertex3f(self.points3DList[face.a].x * scale_from_editor * zoom, self.points3DList[face.a].y * scale_from_editor * zoom, self.points3DList[face.a].z * scale_from_editor * zoom)

            glNormal3f(self.points3DList[face.b].x * scale_from_editor * zoom, self.points3DList[face.b].y * scale_from_editor * zoom, self.points3DList[face.b].z * scale_from_editor * zoom)
            glVertex3f(self.points3DList[face.b].x * scale_from_editor * zoom, self.points3DList[face.b].y * scale_from_editor * zoom, self.points3DList[face.b].z * scale_from_editor * zoom)

            glNormal3f(self.points3DList[face.c].x * scale_from_editor * zoom, self.points3DList[face.c].y * scale_from_editor * zoom, self.points3DList[face.c].z * scale_from_editor * zoom)
            glVertex3f(self.points3DList[face.c].x * scale_from_editor * zoom, self.points3DList[face.c].y * scale_from_editor * zoom, self.points3DList[face.c].z * scale_from_editor * zoom)
        
            glEnd()
