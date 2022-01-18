
from util.Modelo import Modelo
from util.Frustrum import Frustum
from util.Camera import Camera
from util.Material import Material
from util.Spotlight import Spotlight
from util.Planet import Planet
from loaders.Asc_Loader import AscLoader
from OpenGL.GLUT import * 
from OpenGL.GLU import *
from OpenGL.GL import *
import json 
import math
import random
import numpy as np

class Mundo:

    # Distintas opciones del menu.
    opcionesMenu = {
      "FONDO_1":0,
      "FONDO_2":1,
      "FONDO_3":2,
      "DIBUJO_1":3,
      "DIBUJO_2":4,
      "DIBUJO_3":5,
      "FORMA_1":6,
      "FORMA_2":7,
      "FORMA_3":8,
      "FORMA_4":9,
      "CAMARA_1":10,
      "CAMARA_2":11,
      "CAMARA_3":12,
      "CAMARA_4":13,

    }

    #Número de vistas diferentes.
    numCamaras=4

    # Variable que define el tiempo
    t=0

    #Definimos los distintos colores que usaremos para visualizar nuestro Sistema Planetario.
    #Negro, Verde oscuro, Azul oscuro, Blanco, Verde claro, Azul claro
    colores=[(0.00, 0.00, 0.00), (0.06, 0.25, 0.13), (0.10, 0.07, 0.33), (1.00, 1.00, 1.00), (0.12, 0.50, 0.26), (0.20, 0.14, 0.66)]

    def __init__(self):
        #Inicializamos todo:

        #Variables de la clase
        self.width=800
        self.height=800
        self.aspect = self.width/self.height
        self.angulo = 100
        self.window=0

        #variables de tiempo
        self.t = 0
        self.pauseTime = False

        self.planets : Planet = [] # array que contiene a todos los planetas
        self.spotlights : Spotlight = [] # array que contiene todas las luces
        self.spotlightsKey = False # bandera para saber si se ha pulsado la tecla para manejar las luces
        self.cameras : Camera = [] # array que contiene todas las camaras
        self.camerasKey = False # bandera pasa saber si se ha pulsado la tecla para manejar las camaras
        self.activeCamera = 0 # variable para saber que camara está activada
        self.drawOrbits = False # bandera para saber si hay que pintar las orbitas de los planetas
        self.velocityKey = False # bander para saber si se ha pulsado la tecla para manejar el tiempo
        self.velocityExtra = 1 # factor multiplicador de velocidad


        # variables que tienen que ver con las estrellas
        self.numStars = 1000
        self.vStars = []

        #Tamaño de los ejes y del alejamiento de Z.
        self.tamanio=100
        self.z0=0

        #Factor para el tamaño del modelo.
        self.escalaGeneral = 0.005

        #Rotacion de los modelos.
        self.alpha=0
        self.beta=0

        #Variables para la gestion del ratón.
        self.xold=0
        self.yold=0
        self.zoom=1.0

        #Vistas del Sistema Planetario.
        #modelo.tipoVista forma
        self.dibujo=3
        self.fondo=0
        self.forma=9

        self.generateStars() # llamamos para generar las estrellas una sola vez

    def setMoons(self, jMoons):

        moons : Planet = []
        loader = AscLoader()

        if(jMoons != None):
            for m in jMoons:
                moon = Planet(
                        m['inclination'],
                        m['radius'],
                        m['name'],
                        m['wRotAstro'],
                        m['wRotProp'],
                        m['size'],
                        [],
                        Material(
                            m['material']['shine'],
                            m['material']['diffused_light'],
                            m['material']['ambient_light'],
                            m['material']['specular_light']
                        )
                    )
                self.cargarModelo("models/Esfera.asc", moon, loader)
                moons.append(moon)
        
        return moons

    def load(self, file):
        with open(file, encoding="UTF-8") as j:
            world = json.load(j)
            planets = world['planets']
            spotlights = world['spotlights']
            cameras = world['cameras']
            frustum = world['frustum']
            loader = AscLoader()

            for p in planets:
                planet = Planet(
                    p['inclination'],
                    p['radius'],
                    p['name'],
                    p['wRotAstro'],
                    p['wRotProp'],
                    p['size'],
                    self.setMoons(p['moons']),
                    Material(
                        p['material']['shine'],
                        p['material']['diffused_light'],
                        p['material']['ambient_light'],
                        p['material']['specular_light']
                    )
                )
                self.cargarModelo("models/Esfera.asc", planet, loader)
                self.planets.append(planet)

            for s in spotlights:
                sl = Spotlight(
                    s['id'],
                    s['diffused_light'],
                    s['ambient_light'],
                    s['specular_light'],
                    s['location']
                )
                self.spotlights.append(sl)

            self.frustum = Frustum(
                frustum['alpha'],
                frustum['aspect'],
                frustum['near'],
                frustum['far']
            )

            for c in cameras:
                cm = Camera(
                    c['x_axis'],
                    c['y_axis'],
                    c['z_axis'],
                    c['center_x'],
                    c['center_y'],
                    c['center_z'],            
                    c['up_x'],
                    c['up_y'],
                    c['up_z']
                )
                cm.setFrustum(self.frustum)
                self.cameras.append(cm)

    def drawAxis(self):
        #Inicializamos
        glDisable(GL_LIGHTING)
        glBegin(GL_LINES)
	
        #Eje X Rojo
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(self.tamanio, 0.0, 0.0)

        #Eje Y Verde
        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, self.tamanio, 0.0)

        #Eje Z Azul
        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, 0.0, self.tamanio)

        glEnd()
        glEnable(GL_LIGHTING)

    def drawModel(self,modelo : Modelo, escala):
        if(self.forma == 6):
            modelo.drawWired(escala, self.zoom)
        if(self.forma == 7):
            modelo.drawSolid(escala, self.zoom)
        if(self.forma == 8):
            modelo.drawFlat(escala, self.zoom)
        if(self.forma == 9):
            modelo.drawSmooth(escala, self.zoom)

    def display(self):

        glClearDepth(1.0)
        glClearColor(self.colores[self.fondo][0], self.colores[self.fondo][1], self.colores[self.fondo][2], 1.0)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glEnable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        self.cameras[self.activeCamera].on() # encendemos la camara que esta activa

        glRotatef(self.alpha, 1.0, 0.0, 0.0)
        glRotatef(self.beta, 0.0, 1.0, 0.0)

        #Establecemos el color del Modelo.
        glColor3f(self.colores[self.dibujo][0], self.colores[self.dibujo][1], self.colores[self.dibujo][2])
            
        #Dibujamos los ejes de coordenadas
        #self.drawAxis()

        if(not self.pauseTime): self.t += 1 # Aumentamos la variable del tiempo

        self.drawSun() # Dibujamos primeramente el sol
        self.drawPlanets() # Despues dibujamos cada uno de los planetas
        self.drawStars() # pintamos las estrellas
        if(self.drawOrbits): 
            self.drawOrbitsPlanets() # pintamos las orbitas de los planetas

        glFlush()
        glutSwapBuffers()

    def drawSun(self):

        glPushMatrix()
        self.planets[0].material.start()
        self.planets[0].translate(self.t * self.velocityExtra, self.zoom)
        self.planets[0].rotate(self.t)
        glColor3f(self.colores[self.dibujo][0], self.colores[self.dibujo][1], self.colores[self.dibujo][2])
        self.drawModel(self.planets[0], self.escalaGeneral * self.planets[0].size)
        glPopMatrix()

    
    def drawPlanets(self):
        for planet in self.planets[1:]:
            glPushMatrix()
            planet.material.start()
            planet.translate(self.t * self.velocityExtra, self.zoom)
            planet.rotate(self.t)

            if(planet.name == "Saturno"):
                self.drawSaturnRing(planet)

            if(planet.moons != []):
                for moon in planet.moons:
                    self.drawMoon(moon)
                    if(self.drawOrbits):
                        self.drawOrbitMoon(moon)
            
            glColor3f(self.colores[self.dibujo][0], self.colores[self.dibujo][1], self.colores[self.dibujo][2])
            self.drawModel(planet, self.escalaGeneral * planet.size)
            glPopMatrix()

    def drawMoon(self, moon):
        glPushMatrix()
        moon.material.start()
        moon.translate(self.t * self.velocityExtra, self.zoom)
        moon.rotate(self.t)
        glColor3f(self.colores[self.dibujo][0], self.colores[self.dibujo][1], self.colores[self.dibujo][2])
        self.drawModel(moon, self.escalaGeneral * moon.size)
        glPopMatrix()

    def drawSaturnRing(self, saturn):
        glColor3f(91,29,16) # color marrón cafe
        glBegin(GL_LINE_STRIP)
        for i in range(0, 360):
            for j in range(0, 40, 1):
                glVertex3d(
                (110 + j) * self.zoom / 100 * math.cos(saturn.wRotAstro * 2 * i * math.pi / 360), 
                (110 + j) * self.zoom / 100 * math.sin(saturn.wRotAstro * 2 * i * math.pi / 360),
                0)
        glEnd()
        glEnable(GL_LIGHTING)

    def drawOrbitsPlanets(self):
        for planet in self.planets[1:]:
            glColor3f(255, 255, 255)
            glBegin(GL_LINE_STRIP)
            for i in range(0, int(planet.radius)):
                glVertex3d(
                    planet.radius * self.zoom / 100 * math.cos(planet.wRotAstro * 2 * i * math.pi / 360), 
                    0,
                    planet.radius * self.zoom / 100 * math.sin(planet.wRotAstro * 2 * i * math.pi / 360))
            glEnd()
            glEnable(GL_LIGHTING)


    def drawOrbitMoon(self, moon):
        glColor3f(255, 255, 255)
        glBegin(GL_LINE_STRIP)
        for i in range(0, 360):
            glVertex3d(
                moon.radius * self.zoom / 100 * math.cos(moon.wRotAstro * 2 * i * math.pi / 360), 
                0,
                moon.radius * self.zoom / 100 * math.sin(moon.wRotAstro * 2 * i * math.pi / 360))
        glEnd()
        glEnable(GL_LIGHTING)


    def drawStars(self):

        glColor3f(1,1,1)
        glBegin(GL_POINTS)
    
        for s in range(0, self.numStars):
            glVertex3d(
                self.vStars[s][0], 
                self.vStars[s][1],
                self.vStars[s][2]
                )
        
        glEnd()
        glEnable(GL_LIGHTING)


    def generateStars(self):
        for i in range(0,self.numStars):
            star = []
            for j in range(3):
                star.append(self.zoom * random.uniform(-20,20))
            self.vStars.append(star)


    
        
    #Funcion para gestionar los movimientos del raton.
    def onMouse(self, button, state, x, y):
        if (button == 3) or (button == 4):
            if (state == GLUT_UP):
                pass
            if(button==3 and self.zoom > 0.25):
                self.zoom=self.zoom-0.1
                self.vStars.clear() # limpiamos las estrellas
                self.generateStars() # generamos nuevas estrellas
                #print("Zoom negativo...." + str(self.zoom))
            elif(self.zoom < 10):
                self.vStars.clear() # limpiamos las estrellas
                self.generateStars() # generamos nuevas estellas
                self.zoom=self.zoom+0.1
                #print("Zoom positivo...." + str(self.zoom))
        else:
            #Actualizamos los valores de x, y.
            self.xold = x
            self.yold = y 

    #Funcion que actualiza la posicion de los modelos en la pantalla segun los movimientos del raton.
    def onMotion(self, x, y):
        self.alpha = (self.alpha + (y - self.yold))
        self.beta = (self.beta + (x - self.xold))
        self.xold = x
        self.yold = y
        glutPostRedisplay()

    #Funcion que gestiona las pulsaciones en el teclado.
    def keyPressed(self, key, x, y):
        key = unicode(key, 'utf-8')
        
        if(key == 'q'):  #Tecla Esc
            #Cerramos la ventana y salimos
            os._exit(0)

        if(key == 'p'):
            self.pauseTime = not self.pauseTime
        
        if(key == 'f'):
            self.spotlightsKey = True

        if(key == 'c'):
            self.camerasKey = True

        if(key == 'o'):
            self.drawOrbits = not self.drawOrbits

        if(key == 't'):
            self.velocityKey = not self.velocityKey

        if(self.velocityKey):
            if(key == '+'):
                self.velocityExtra += 0.01
            if(key == '-' and self.velocityExtra > 0):
                self.velocityExtra -= 0.01

        if(key == '1'):
            if(self.spotlightsKey):
                if(glIsEnabled(GL_LIGHT0 + self.spotlights[0].id)):
                    self.spotlights[0].off()
                else:
                    self.spotlights[0].on()
                
                self.spotlightsKey = False

            if(self.camerasKey):
                self.activeCamera = 0
                self.camerasKey = False

        if(key == '2'):
            if(self.spotlightsKey):
                if(glIsEnabled(GL_LIGHT0 + self.spotlights[1].id)):
                    self.spotlights[1].off()
                else:
                    self.spotlights[1].on()

                self.spotlightsKey = False

            if(self.camerasKey):
                self.activeCamera = 1
                self.camerasKey = False

        if(key == '3'):
            if(self.spotlightsKey):
                if(glIsEnabled(GL_LIGHT0 + self.spotlights[2].id)):
                    self.spotlights[2].off()
                else:
                    self.spotlights[2].on()

                self.spotlightsKey = False
        
            if(self.camerasKey):
                self.activeCamera = 2
                self.camerasKey = False

        if(key == '4'):
            if(self.spotlightsKey):
                if(glIsEnabled(GL_LIGHT0 + self.spotlights[3].id)):
                    self.spotlights[3].off()
                else:
                    self.spotlights[3].on()

                self.spotlightsKey = False

            if(self.camerasKey):
                self.activeCamera = 3
                self.camerasKey = False
            

        if(key == '5'):
            if(self.spotlightsKey):
                if(glIsEnabled(GL_LIGHT0 + self.spotlights[4].id)):
                    self.spotlights[4].off()
                else:
                    self.spotlights[4].on()

                self.spotlightsKey = False
                
        if(key == '6'):
            if(self.spotlightsKey):
                if(glIsEnabled(GL_LIGHT0 + self.spotlights[5].id)):
                    self.spotlights[5].off()
                else:
                    self.spotlights[5].on()

                self.spotlightsKey = False

        if(key == '7'):
            if(self.spotlightsKey):
                if(glIsEnabled(GL_LIGHT0 + self.spotlights[6].id)):
                    self.spotlights[6].off()
                else:
                    self.spotlights[6].on()

                self.spotlightsKey = False

        if(key == '8'):
            if(self.spotlightsKey):
                if(glIsEnabled(GL_LIGHT0 + self.spotlights[7].id)):
                    self.spotlights[7].off()
                else:
                    self.spotlights[7].on()

                self.spotlightsKey = False

        if(key == '0'):
            if(self.spotlightsKey):
                for s in self.spotlights:
                    s.off()
                self.spotlightsKey = False
  
    #Funcion para activar las distintas opciones que permite el menu.
    def onMenu(self, opcion):
        if(opcion == self.opcionesMenu["FONDO_1"]):
            self.fondo = 0
        elif(opcion == self.opcionesMenu["FONDO_2"]):
            self.fondo = 1
        elif(opcion == self.opcionesMenu["FONDO_3"]):
            self.fondo = 2
        elif(opcion == self.opcionesMenu["DIBUJO_1"]):
            self.dibujo = 3
        elif(opcion == self.opcionesMenu["DIBUJO_2"]):
            self.dibujo = 4
        elif(opcion == self.opcionesMenu["DIBUJO_3"]):
            self.dibujo = 5
        elif(opcion == self.opcionesMenu["FORMA_1"]):
            self.forma = 6
        elif(opcion == self.opcionesMenu["FORMA_2"]):
            self.forma = 7
        elif(opcion == self.opcionesMenu["FORMA_3"]):
            self.forma = 8
        elif(opcion == self.opcionesMenu["FORMA_4"]):
            self.forma = 9
        elif(opcion == self.opcionesMenu["CAMARA_1"]):
            self.activeCamera = 0
        elif(opcion == self.opcionesMenu["CAMARA_2"]):
            self.activeCamera = 1
        elif(opcion == self.opcionesMenu["CAMARA_3"]):
            self.activeCamera = 2
        elif(opcion == self.opcionesMenu["CAMARA_4"]):
            self.activeCamera = 3
        glutPostRedisplay()
        return opcion
   
    def cargarModelo(self, name, model : Modelo, loader):
        _, vertices, faces = loader.load(name)
        model.numVertices = len(vertices)
        model.numCaras = len(faces)
        model.facesList = faces
        model.points3DList = vertices