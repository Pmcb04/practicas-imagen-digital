

class States:

    state = (1, 1)  # (1,1): Dentro | (1,0): Saliendo | (0,1): Entrando | (0,0): Fuera

    '''
    Método que cambia el estado del sistema, estos estados están codificado de la forma:
    (0,0): Se encuentra fuera del aula
    (0,1): Se encuentra entrando en el aula
    (1,0): Se encuentra saliendo del aula
    (1,1): Se encuentra dentro del aula
    '''
    
    def changeState(self, cY, lowerLine, upperLine, counter):
        if cY < upperLine:


            # Encima de la línea de arfriba (dentro)
            if self.state == (1, 0):
                # Pasa de estado (0,1) a estado (1,1) (medio a arriba)
                print("Dentro")
                self.state = (1, 1)

            elif self.state == (0, 1):
                # Pasa de estado (0,1) a estado (1,1) (medio a arriba)
                print("Dentro")
                self.state = (1, 1)
                counter += 1
                #MainWindow.counter.setText("Contador: " + str(counter))
                print(counter)

        elif cY > upperLine and cY < lowerLine:

            # Entre ambas barreras (entrando o saliendo)
            if self.state == (1, 1):
                # Pasa de estado (1,1) a estado (1,0) (arriba a medio)
                print("Saliendo")
                self.state = (1, 0)
           
            elif self.state == (0, 0):
                # Pasa de estado (0,0) a estado (0,1) (abajo a medio)
                print("Entrando")
                self.state = (0, 1)
        
        elif cY > lowerLine:
            
            # Debajo de la línea de abajo (fuera)
            if self.state == (1, 0):
                # Pasa de estado (1,0) a estado (0,0) (medio a abajo)
                print("Fuera")
                self.state = (0, 0)
                counter -= 1
                #MainWindow.counter.setText("Contador: " + str(counter))
                print(counter)
            
            elif self.state == (0, 1):
                # Pasa de estado (1,0) a estado (0,0) (medio a abajo)
                print("Fuera")
                self.state = (0, 0)

        return counter