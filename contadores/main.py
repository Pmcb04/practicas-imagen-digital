import sys
from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QFileDialog
import cv2
import numpy as np
import math
import matchTemplate as mt
from matplotlib import pyplot as plt

WIDTH_CONT=304 
HEIGHT_CONT=130

WIDTH_TEMPLATE=90 
HEIGHT_TEMPLATE=130

DECIMAL_CARACTER = "."

rectangleAreas = [  # x, y, ancho, alto
    (1030, 564, 400, 140),
    (1030, 850, 400, 140),
    (1030, 1144, 400, 140)
]

class Window:

    def __init__(self):
        # Cargamos la pantalla principal
        self.MainWindow = uic.loadUi('mainwindow.ui')
        # Establecemos un título a la pantalla principal
        self.MainWindow.setWindowTitle("Looking for something")

        # clipping button
        self.MainWindow.Clip_button.clicked.connect(self.clipping)

        # load button
        self.MainWindow.Load_button.clicked.connect(self.loadImage)

        # extract number button and windows
        self.MainWindow.OCR_button.clicked.connect(self.extractNumbers)

        self.res1 = self.MainWindow.resultado1
        self.res2 = self.MainWindow.resultado2
        self.res3 = self.MainWindow.resultado3

        # image of individual counters cropped
        self.cropped1 = ""
        self.cropped2 = ""
        self.cropped3 = ""

        # global process button
        self.MainWindow.GLOBAL_button.clicked.connect(self.globalProcess)

    def globalProcess(self):
        self.loadImage()
        self.clipping()
        self.extractNumbers()

    def loadImage(self):
        
        directory = "capturas"
        fn = QFileDialog.getOpenFileName(self.MainWindow, "Choose a frame to download", directory,
                                            "Images (*.png *.xpm *.jpg)")
        img_fn = str(fn[0])

        if(img_fn != ""):

            self.original_image = cv2.imread(img_fn, cv2.IMREAD_COLOR)
            self.mat_original = cv2.resize(self.original_image, (720, 540), cv2.INTER_CUBIC)

            self.cleanLabels()

            image = QtGui.QImage(self.mat_original, 720, 540, QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap()
            pixmap.convertFromImage(image.rgbSwapped())
            self.MainWindow.viewer_original.setPixmap(pixmap)

    def clipping(self):
    
        self.cleanLabels()

        for i in range(len(rectangleAreas)):
            x, y, w, h = rectangleAreas[i][0], rectangleAreas[i][1], rectangleAreas[i][2], rectangleAreas[i][3]
            self.cropped = self.original_image[y:y + h, x:x + w]
            self.cropped = cv2.resize(self.cropped, (WIDTH_CONT, HEIGHT_CONT), cv2.INTER_CUBIC)

            if i == 0: # contador 1
                self.cropped1 = self.cropped
                self.image_counter1 = QtGui.QImage(self.cropped, WIDTH_CONT, HEIGHT_CONT, QtGui.QImage.Format_RGB888)
                pixmap = QtGui.QPixmap()
                pixmap.convertFromImage(self.image_counter1.rgbSwapped())
                self.MainWindow.viewer_counter1.setPixmap(pixmap)

            elif i == 1: # contador 2
                self.cropped2 = self.cropped
                self.image_counter2 = QtGui.QImage(self.cropped, WIDTH_CONT, HEIGHT_CONT, QtGui.QImage.Format_RGB888)
                pixmap = QtGui.QPixmap()
                pixmap.convertFromImage(self.image_counter2.rgbSwapped())
                self.MainWindow.viewer_counter2.setPixmap(pixmap)

            elif i == 2: # contador 3 
                self.cropped3 = self.cropped
                self.image_counter3 = QtGui.QImage(self.cropped, WIDTH_CONT, HEIGHT_CONT, QtGui.QImage.Format_RGB888)
                pixmap = QtGui.QPixmap()
                pixmap.convertFromImage(self.image_counter3.rgbSwapped())
                self.MainWindow.viewer_counter3.setPixmap(pixmap)


    def extractNumbers(self):

        num1 = ""
        num2 = ""
        num3 = ""

        self.clearNumbers()

        for i in range(0,4):
            x, y, w, h = i*int(WIDTH_CONT/4), 0, int(WIDTH_CONT/4), HEIGHT_CONT
            num_cropped = self.cropped1[y:y + h, x:x + w]
            num_cropped = cv2.resize(num_cropped, (WIDTH_TEMPLATE, HEIGHT_TEMPLATE), cv2.INTER_CUBIC)
            num_cropped = cv2.cvtColor(num_cropped, cv2.COLOR_BGR2GRAY) # ponemos la imagen en b&w para compararla con los templates
            num1 += mt.MatchTemplate().doMatch(num_cropped)

            num_cropped = self.cropped2[y:y + h, x:x + w]
            num_cropped = cv2.resize(num_cropped, (WIDTH_TEMPLATE, HEIGHT_TEMPLATE), cv2.INTER_CUBIC)
            num_cropped = cv2.cvtColor(num_cropped, cv2.COLOR_BGR2GRAY) # ponemos la imagen en b&w para compararla con los templates
            num2 += mt.MatchTemplate().doMatch(num_cropped)

            num_cropped = self.cropped3[y:y + h, x:x + w]
            num_cropped = cv2.resize(num_cropped, (WIDTH_TEMPLATE, HEIGHT_TEMPLATE), cv2.INTER_CUBIC)
            num_cropped = cv2.cvtColor(num_cropped, cv2.COLOR_BGR2GRAY) # ponemos la imagen en b&w para compararla con los templates
            num3 += mt.MatchTemplate().doMatch(num_cropped)

            # añadimos el punto para separar los decimales
            if(i == 2): 
                num1 += DECIMAL_CARACTER  
                num2 += DECIMAL_CARACTER
                num3 += DECIMAL_CARACTER

        self.res1.append(num1)
        self.res2.append(num2)
        self.res3.append(num3)

    def cleanLabels(self):
        self.MainWindow.viewer_counter1.clear()
        self.MainWindow.viewer_counter2.clear()
        self.MainWindow.viewer_counter3.clear()
        self.clearNumbers()

    def clearNumbers(self):
        self.res1.clear()
        self.res2.clear()
        self.res3.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.MainWindow.show()
    app.exec_()
