import math
import cv2

# Metodo que indica si todos los angulos de una figura son rectos
def calcularAngRecto(result):
    resultado = False

    if 86<= result[0] <= 92 and 86<= result[1] <= 92 and 86<= result[2] <= 92:
        resultado = True
    elif 86<= result[3] <= 92 and 86<= result[0] <= 92 and 86<= result[1] <= 92:
        resultado = True
    elif 86<= result[2] <= 92 and 86<= result[3] <= 92 and 86<= result[0] <= 92:
        resultado = True

    return resultado

# Metodo que indica si los angulos de una figura son todos diferentes
def angDifferent(result):
    return result[0] != result[1] != result[2] != result[3] 

# Metodo que indica si los angulos pares de una figura son rectos
def calcularTwoConsecutiveAngRecto(result):
    resultado = False

    if (86<= result[0] <= 92 or 86<= result[1] <= 92) and ((result[2] < 86 or result[2] > 92) or (result[3] < 86 or result[3] > 92) ):
        resultado = True
    if (86<= result[1] <= 92 or 86<= result[2] <= 92) and ((result[3] < 86 or result[3] > 92) or (result[0] < 86 or result[0] > 92) ):
        resultado = True
    if (86<= result[2] <= 92 or 86<= result[3] <= 92) and ((result[0] < 86 or result[0] > 92) or (result[1] < 86 or result[1] > 92) ):
        resultado = True
    if (86<= result[3] <= 92 or 86<= result[0] <= 92) and ((result[1] < 86 or result[1] > 92) or (result[2] < 86 or result[2] > 92) ):
        resultado = True

    return resultado

# Metodo que indica si al menos dos angulos pares de una figura son rectos
def calcularAngRectoPares(result):
    resultado = False

    if 86<= result[0] <= 92 and 86<= result[1] <= 92:
        resultado = True
    if 86<= result[1] <= 92 and 86<= result[2] <= 92:
        resultado = True
    if 86<= result[2] <= 92 and 86<= result[3] <= 92:
        resultado = True

    return resultado

# Metodo que devuelve un angulo dados tres puntos
def getAngle(PointA, PointB, PointC):
    dot = ((PointA[0][0] - PointB[0][0]) * (PointC[0][0] - PointB[0][0]) + (
                (PointA[0][1] - PointB[0][1]) * (PointC[0][1] - PointB[0][1])))
    pcross = ((PointA[0][0] - PointB[0][0]) * (PointC[0][1] - PointB[0][1]) - (PointA[0][1] - PointB[0][1]) * (
                PointC[0][0] - PointB[0][0]))
    angle = math.fabs(cv2.fastAtan2(float(pcross), float(dot)))
    return angle

# Metodo que devuelve todos los angulos de una figura
def findAngles(p1, p2, p3, p4):
    a = getAngle(p1, p2, p3)
    b = getAngle(p2, p1, p4)
    c = getAngle(p2, p3, p4)
    d = getAngle(p3, p4, p1)
    return a, b, c, d

# Metodo que duelve el rango de un angulo
def rangeAngles(angle, low, high):
    result = low <= ((angle*180) / 3.141592) <= high
    return result

# Metodo que calcula un angulo dado tres puntos
def angulo(p1, p2, p0):
    dx1 = math.fabs(p1[0][0] - p0[0][0])
    dy1 = math.fabs(p1[0][1] - p0[0][1])
    dx2 = math.fabs(p2[0][0] - p0[0][0])
    dy2 = math.fabs(p2[0][1] - p0[0][1])
    return (dx1 * dx2 + dy1 * dy2) / math.sqrt((dx1 * dx1 + dy1 * dy1) * (dx2 * dx2 + dy2 * dy2) + 1e-10);

# Metodo que mide la distancia entre dos puntos
def distancias(p1, p2):
    x1 = p2[0][0]
    x0 = p1[0][0]
    y1 = p2[0][1]
    y0 = p1[0][1]
    return round(math.sqrt(math.pow(x1 - x0, 2) + math.pow(y1 - y0, 2)))

#Metodo que indica si todos los vertices de una figura tienen la misma distancia
def ladosIguales (approx):
    a = distancias(approx[0], approx[1])
    b = distancias(approx[1], approx[2])
    c = distancias(approx[2], approx[3])
    d = distancias(approx[3], approx[0])
    return normalizar(a,b) and normalizar(b,c) and normalizar(c,d) and normalizar(d,a)

#Metodo que indica si todos los vertices de una figura tienen la misma distancia
def ladosParesIguales (approx):
    a = distancias(approx[0], approx[1])
    b = distancias(approx[1], approx[2])
    c = distancias(approx[2], approx[3])
    d = distancias(approx[3], approx[0])
    return ( normalizar(a,c) ) or ( normalizar(b, d) ) 

#Metodo para normalizar un dato
def normalizar (p1, p2):
    return 0.95 <= p1/p2 <= 1.05

#Metodo que devuelve el tipo de figura geometrica que es un contorno dado
def typeContours (c, approx):
    type = ""
    if len(approx) == 3: #Si el numero de vertices detectados es 3 se trata de un triangulo
        type = "Triangulo"

    if len(approx) == 4:  #Si el numero de vertices detectados es 4 es un tipo de cuadrilatero
        p1 = approx[0]
        p2 = approx[1]
        p3 = approx[2]
        p4 = approx[3]
        result = findAngles(p1, p2, p3, p4)

        if ladosIguales(approx) and calcularAngRecto(result):
            type = "Cuadrado"
        elif calcularAngRecto(result) and (not (ladosIguales(approx))):
            type = "Rectangulo"
        elif (ladosIguales(approx) and (not calcularAngRecto(result))):
            type = "Rombo"
        elif((not ladosIguales(approx)) and calcularTwoConsecutiveAngRecto(result)):
            type = "Trapecio rectangulo"
        elif((not ladosIguales(approx)) and ladosParesIguales(approx)):
            type = "Trapecio isosceles"
        elif((not ladosIguales(approx)) and angDifferent(result)):
            type = "Trapecio escaleno"
        else:
            type = "Cuadrilatero"

    if len(approx) == 5: #Si el numero de vertices detectados es 5 se trata de un pentagono
        type = "Pentagono"
    if len(approx) == 6: #Si el numero de vertices detectados es 6 se trata de un hexagono
        type = "Hexagono"
    if len(approx) > 10: #Si el numero de vertices detectados es mayor que 10 concluimos que es un circulo
        type = "Circulo"

    return type