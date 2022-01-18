# Autores: David Merino Vecino y Ainhoa Martinez Horrillo

import cv2
import metodos

def on_change(self): # No hace nada, pero se debe pasar la funcion a cv2.createTrackbar
    pass

# Lectura de la imagen original
cap = cv2.imread('imagenes/prueba3.png')

# Creacion de una ventana para agregar trackbars
cv2.namedWindow('Canny', cv2.WINDOW_AUTOSIZE)

# Definicion de los valores iniciales y maximos de cada trackbar
c_lower_l, c_lower_u = 85, 255 # Limite inferior para la deteccion de bordes con canny
c_upper_l, c_upper_u = 230, 255 # Limite superior para la deteccion de bordes con canny
blur_s, blur_f = 1, 15 # Desenfoque Gaussiano

# Creacion de trackbars
cv2.createTrackbar("Canny Limit Lower", "Canny", c_lower_l, c_lower_u, on_change) # Limite inferior canny
cv2.createTrackbar("Canny Limit Upper", "Canny", c_upper_l, c_upper_u, on_change) # Limite superior canny
cv2.createTrackbar("Gaussian Blur", "Canny", blur_s, blur_f, on_change) # Desenfoque Gaussiano

cv2.startWindowThread() # Inicio de la ventana

while (True):
    l = cv2.getTrackbarPos("Canny Limit Lower", "Canny") # Limite inferior canny
    u = cv2.getTrackbarPos("Canny Limit Upper", "Canny") # Limite superior canny
    b = cv2.getTrackbarPos("Gaussian Blur", "Canny") # Desenfoque Gaussiano

    if b == 0: # Para que no se produzca un error
        b = 1

    img = cap.copy()

    # Conversion de la imagen original a escala de grises
    gray = cv2.cvtColor(cap, cv2.COLOR_BGR2GRAY)

    # Desenfoque Gaussiano
    gaussian = cv2.blur(gray, (b, b))

    # Obtencion de la imagen binarizada a traves de la deteccion de bordes con canny
    canny = cv2.Canny(gaussian, l, u, L2gradient=True)

    cv2.imshow('Canny', canny)

    # Busqueda de contornos
    contornos, _ = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Bucle para identificar la figura geometrica de cada cotorno encontrado
    for c in contornos:
        epsilon = 0.01 * cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, epsilon, True) # Aproximacion del contorno

        x, y, w, h = cv2.boundingRect(approx)
        type = metodos.typeContours(c, approx) # Metodo que devuelve el tipo de figura geometrica
        cv2.putText(img, type, (x, y - 5), 1, 1, (0, 255, 0), 1)

        cv2.drawContours(img, [approx], -1, (0, 255, 0), 2)
        cv2.imshow("Contornos", img)

    if cv2.waitKey(1) == 27: # Pulsacion de la tecla ESC para salir
        break

cv2.destroyAllWindows()
