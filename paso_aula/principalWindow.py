from PyQt5 import uic,QtGui,QtCore
import cv2
import imutils
from states import States

MAX_SPEED=100

class PrincipalWindow:
    cap = cv2.VideoCapture('video.wmv')
    ret, originalFrame = cap.read()
    ventanasMostrar = False
    fps = 60
    pause = False
    states = States()

    #state = (1, 1)  # (1,1): Dentro | (1,0): Saliendo | (0,1): Entrando | (0,0): Fuera
    counter = 1

    def __init__(self):

        # Carga de la ventana principal
        self.MainWindow = uic.loadUi('mainwindow.ui')

        # Poner título a la ventana 
        self.MainWindow.setWindowTitle("Paso de Aula")

        # Mostrar el contador de personas
        self.MainWindow.counter.setText('Cont: ' + str(self.counter))

        # Cambiar velocidad de vídeo
        self.MainWindow.spinSpeed.setValue(self.fps)
        self.MainWindow.spinSpeed.valueChanged.connect(self.speed)
        
        # Pausar video
        self.MainWindow.buttonPause.clicked.connect(self.onPause)
        
        # Mostrar todas las ventanas
        self.MainWindow.buttonDebug.clicked.connect(self.debug)
        self.MainWindow.buttonCloseDebug.clicked.connect(self.closeWindows)
        
        # Recargar el programa
        self.MainWindow.buttonRestart.clicked.connect(self.restart)

        
        self.timer_frames = QtCore.QTimer(self.MainWindow)
        self.timer_frames.timeout.connect(self.gmg)  # timer para refrescar la ventana
        self.timer_frames.start(self.fps)

    #Método que cierra las ventanas con los diferentes vídeos
    def closeWindows(self):
        self.ventanasMostrar = False
        cv2.destroyAllWindows()
        

    #Método que reinicia el vídeo del aula
    def restart(self):
        self.closeWindows()
        self.counter = 1
        self.cap = cv2.VideoCapture('video.wmv')
        self.timer_frames.start()

    #Método que controla la velocidad del vídeo en orden ascendente
    def speed(self):
        self.timer_frames.setInterval(MAX_SPEED-self.MainWindow.spinSpeed.value())

    #Método que pausa el vídeo temporalmente
    def onPause(self):
        if not self.pause:
            self.timer_frames.stop()
            self.pause = True
        else:
            self.timer_frames.start()
            self.pause = False

    #Método que muestra las diferentes ventanas con los diferentes pasos del proceso
    def debug(self):
        self.ventanasMostrar = True

    #Método que muestra la ventana principal
    def show(self):
        self.MainWindow.show()

    #Este método se encarga de crear parte por parte el proceso completo que dará como resultado
    #la detección de si la persona atraviesa las barreras hacia dentro o fuera del aula
    def gmg(self):

        ret, frame = self.cap.read()
        if (ret):
            
            # Imagen en blanco y negro de referencia
            referenceGreyImage = cv2.cvtColor(self.originalFrame, cv2.COLOR_BGR2GRAY)
            # Escala de gris actual
            currentGreyImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Imagen de diferencia absoluta
            diff = cv2.absdiff(currentGreyImage, referenceGreyImage)

            # ret:
            endImage = frame

            # Thresholding Difference Image
            blurredImage = cv2.GaussianBlur(diff, (5, 5), 0)
            thresholdImage = cv2.threshold(blurredImage, 100, 255, cv2.THRESH_BINARY)[1]

            # Centroide. Fuente: https://www.learnopencv.com/find-center-of-blob-centroid-using-opencv-cpp-python/
            cnts = cv2.findContours(thresholdImage.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)

            lowerLine = int((35 * 80 / 10))
            upperLine = int((35 * 65 / 10))

            if (len(cnts) != 0):
                c = max(cnts, key=cv2.contourArea)

                M = cv2.moments(c)
                cX = int(M["m10"] / (M["m00"] + 0.00005))
                cY = int(M["m01"] / (M["m00"] + 0.00005))

                # Dibujar el contorno de la persona y el centroide
                cv2.drawContours(endImage, [c], -1, (93, 208, 201), 1)
                cv2.circle(endImage, (cX, cY), 7, (182, 0, 2251), -1)

                # Punto de reescala
                cY = int(cY / 200 * 350)

                # Procesar estado del punto
                self.counter = self.states.changeState(cY, lowerLine, upperLine, self.counter)
                self.MainWindow.counter.setText('Cont: ' + str(self.counter))

            endImage = cv2.resize(endImage, (500, 350))

            cv2.line(endImage, (0, lowerLine), (500, lowerLine), (180, 0, 0), 2)
            cv2.line(endImage, (0, upperLine), (500, upperLine), (0, 180, 0), 2)
            image = QtGui.QImage(endImage, endImage.shape[1], endImage.shape[0], endImage.shape[1] * 3,
                                 QtGui.QImage.Format_RGB888)

            pix = QtGui.QPixmap(image)

            self.MainWindow.video_source.setPixmap(pix)

            if self.ventanasMostrar:
                cv2.imshow('Video Real', frame)
                cv2.imshow('Imagen Diferencia Absoluta', diff)
                cv2.imshow('Imagen de Umbral', thresholdImage)
                cv2.imshow('Imagen en Gris de Referencia', referenceGreyImage)
                cv2.imshow('Imagen en Escala de Grises Actual', currentGreyImage)
                
                
        else:
            self.MainWindow.video_source.setText("El vídeo ha finalizado")
            self.closeWindows()
            self.timer_frames.stop()

    
