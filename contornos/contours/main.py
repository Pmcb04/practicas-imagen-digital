# Autores: David Merino Vecino y Ainhoa Martinez Horrillo

import cv2
import numpy as np
import metodos

def detect_color(bajo1, alto1, bajo2, alto2):
    # Imagen modo resalte 
    frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frameGray = cv2.cvtColor(frameGray, cv2.COLOR_GRAY2BGR)
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Detectamos el color 
    maskColor1 = cv2.inRange(frameHSV, bajo1, alto1)
    maskColor2 = cv2.inRange(frameHSV, bajo2, alto2)
    mask = cv2.add(maskColor1,maskColor2)
    mask = cv2.medianBlur(mask, 7)
    colorDetected = cv2.bitwise_and(frame,frame,mask=mask)

	# Fondo en grises
    invMask = cv2.bitwise_not(mask)
    bgGray = cv2.bitwise_and(frameGray,frameGray,mask=invMask)
	
	# Sumamos bgGray y redDetected
    return cv2.add(bgGray,colorDetected)


def on_change(self): # No hace nada, pero se debe pasar la funcion a cv2.createTrackbar
    pass

# Captura de la imagen
cap = cv2.VideoCapture(0)

# Creacion de una ventana para agregar trackbars
cv2.namedWindow('Canny', cv2.WINDOW_AUTOSIZE)


cv2.namedWindow('Gray', cv2.WINDOW_AUTOSIZE)

cv2.namedWindow('Gaussian', cv2.WINDOW_AUTOSIZE)

cv2.namedWindow('Settings', cv2.WINDOW_NORMAL)

# Definicion de los valores iniciales y maximos de cada trackbar
c_lower_l, c_lower_u = 85, 255 # Limite inferior para la deteccion de bordes con canny
c_upper_l, c_upper_u = 230, 255 # Limite superior para la deteccion de bordes con canny
blur_s, blur_f = 1, 15 # Desenfoque Gaussiano


rojoBajo1 = np.array([0, 140, 90], np.uint8)
rojoAlto1 = np.array([8, 255, 255], np.uint8)
rojoBajo2 = np.array([160, 140, 90], np.uint8)
rojoAlto2 = np.array([180, 255, 255], np.uint8)

verdeBajo1 = np.array([40, 140, 90], np.uint8)
verdeAlto1 = np.array([55, 255, 255], np.uint8)
verdeBajo2 = np.array([56, 140, 90], np.uint8)
verdeAlto2 = np.array([70, 255, 255], np.uint8)

azulBajo1 = np.array([93, 140, 90], np.uint8)
azulAlto1 = np.array([110, 255, 255], np.uint8)
azulBajo2 = np.array([111, 140, 90], np.uint8)
azulAlto2 = np.array([125, 255, 255], np.uint8)

# Creacion de trackbars 
cv2.createTrackbar("Canny Limit Lower", "Settings", c_lower_l, c_lower_u, on_change) # Limite inferior canny
cv2.createTrackbar("Canny Limit Upper", "Settings", c_upper_l, c_upper_u, on_change) # Limite superior canny
cv2.createTrackbar("Gaussian Blur", "Settings", blur_s, blur_f, on_change) # Desenfoque Gaussiano

cv2.startWindowThread() # Inicio de la ventana 

# Pre-preprocessing should be done here
_, last_ghost = cap.read()
while (True):
    l = cv2.getTrackbarPos("Canny Limit Lower", "Settings")  # Limite inferior canny
    u = cv2.getTrackbarPos("Canny Limit Upper", "Settings")  # Limite superior canny
    b = cv2.getTrackbarPos("Gaussian Blur", "Settings")  # Desenfoque Gaussiano

    if b == 0: # Para que no se produzca un error
        b = 1

    _, frame = cap.read()
    ghost = frame
    fps = cap.get(cv2.CAP_PROP_FPS)
    ret, img = cap.read()

    # Conversion de la imagen original a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Gray', gray)
    
    # Desenfoque Gaussiano
    gaussian = cv2.blur(frame, (b, b))
    cv2.imshow('Gaussian', gaussian)

    # Obtencion de la imagen binarizada a traves de la deteccion de bordes con canny
    canny = cv2.Canny(frame, l, u, L2gradient=True)
    cv2.imshow('Canny', canny)

    # Imagen procesada en modo espejo
    flip = cv2.flip(frame, 1)
    cv2.imshow('Flip', flip)

    # Imagen con efecto ghost 
    if ghost.shape == last_ghost.shape:
        ghost = cv2.addWeighted(src1=frame, alpha=0.5, src2=last_ghost, beta=0.5, gamma=0.0)

    cv2.imshow("Ghost", ghost)

    # Update last_frame
    last_ghost = ghost

	# Detectamos color rojo en la imagen
    cv2.imshow('Red', detect_color(rojoBajo1, rojoAlto1, rojoBajo2, rojoAlto2))

    # Detectamos color verde en la imagen
    cv2.imshow('Green', detect_color(verdeBajo1, verdeAlto1, verdeBajo2, verdeAlto2))

    # Detectamos color verde en la imagen
    cv2.imshow('Blue', detect_color(azulBajo1, azulAlto1, azulBajo2, azulAlto2))

    # Detectamos los contornos de la imagen que estamos procesando
    contornos, _ = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contornos:
        epsilon = 0.01 * cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, epsilon, True) # Aproximacion del contorno

        x, y, w, h = cv2.boundingRect(approx)
        type = metodos.typeContours(c, approx) # Metodo que devuelve el tipo de figura geometrica
        cv2.putText(frame, type, (x, y - 5), 1, 1, (0, 255, 0), 1)

        cv2.drawContours(frame, [approx], -1, (0, 255, 0), 2)


    cv2.imshow('Contours', frame)

    # contours,hierarchy = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(imagen, contornos, -1, (0,255,0), 3)5
    # cv2.imshow('Contours', gaussian)

    if cv2.waitKey(1) == 27: # Pulsacion de la tecla ESC para salir
        break

cap.release()
cv2.destroyAllWindows()