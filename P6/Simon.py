from PyQt6 import QtCore,QtGui,QtWidgets
from Ui_Simon import *
from Ui_PrincipalSimon import *
from Ui_Instrucciones import *
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QWidget, QApplication
'''Libreria para hacer uso de un nuevo hilo'''
from PyQt6.QtCore import QThread, pyqtSignal
import sys
import pyfirmata
import time
import inspect
import random as rand

 

        
class Principal(QMainWindow, Ui_PrincipalSimon):
    
    def __init__(self, *parent, **flags) -> None:
        super().__init__(*parent, **flags)
        self.setupUi(self)

        self.ventana=MainWindow()
        self.instruc=Instrucciones()

        self.pushButton.clicked.connect(self.jugar)
        self.pushButton_2.clicked.connect(self.instrucciones)
        #self.simongame_thread = SimonGameThread()  # Instancia del hilo del juego
        
    def jugar(self):
        self.ventana.show()
        self.close()
    
    def instrucciones(self):
        self.instruc.show()
        



class MainWindow(QMainWindow, Ui_MainWindow,):
    
    def __init__(self, *parent, **flags) -> None:
        super().__init__(*parent, **flags)
        self.setupUi(self)
        
        
        self.Apagarbtn.clicked.connect(self.apagado)
        self.perderbtn.clicked.connect(self.mensage)
        self.Regresarbtn.clicked.connect(self.regresar)
        self.iniciobtn.clicked.connect(self.start_game)
        self.Rojobtn.clicked.connect(self.rojo)
        self.Amarillobtn.clicked.connect(self.amarillo)
        
        '''Conexion de el hilo SimonGameThread'''
        self.simongame_thread=SimonGameThread(self) #Instancia
        
        '''Implementacion de slots para la comunicacion con el hilo externo'''
        self.simongame_thread.signal_azul.connect(self.azul)
        self.simongame_thread.signal_rojo.connect(self.rojo)
        self.simongame_thread.signal_verde.connect(self.verde)
        self.simongame_thread.signal_amarillo.connect(self.amarillo)
        self.simongame_thread.signal_apagado.connect(self.apagado)
        
        '''Reinicio del juego'''
        self.simongame_thread.finished.connect(self.game_finished)  #Conexion con el final del juego
     

    def rojo(self):
        print('ROJO')
        for Qlabel in self.findChildren(QWidget):
            if Qlabel is not self.Rojo:
                Qlabel.lower()
        self.Rojo.raise_()
        print('Ya paso lo feo')
        

    def amarillo(self):
        for Qlabel in window.findChildren(QWidget):
            if Qlabel is not self.Amarillo:
                Qlabel.lower()
        self.Amarillo.raise_()
        
    
    def azul(self):
        print('Boton azul en pantalla')
        for Qlabel in window.findChildren(QWidget):
            if Qlabel is not self.Azul:
                Qlabel.lower()
        self.Azul.raise_()
        print('fin')


    def verde(self):
        for Qlabel in window.findChildren(QWidget):
            if Qlabel is not self.Verde:
                Qlabel.lower()
        self.Verde.raise_()
    
    
    def apagado(self):
        for Qlabel in window.findChildren(QWidget):
            if Qlabel is not self.Apagada:
                Qlabel.lower()
        self.Apagada.raise_()
    
    
    def mensage(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Mensaje")
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setText("Perdiste")
        msg.setInformativeText(f"Lo siento.Perdiste")
        #msg.setDetailedText("Saluditos")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        res = msg.exec()
        print(res)


    def regresar(self):
        window.show()
        self.close()
        
    
    def clickbtn(self):
        print("Esto simula el pulsado")
        self.Rojobtn.click()
        print("Fin del pusheo")
        
        
    def start_game(self):
        self.simongame_thread.start()  # Iniciar el hilo del juego
    
    
    def game_finished(self):
        print("El juego ha terminado")  # Lógica después de que el juego ha finalizado

class SimonGameThread(QThread):
    """Clase que establece un nuevo en la GUI (Principal)

    Args:
        QThread (Funcion): Creacion del hilo
    """
    
    
    def __init__(self, main_window_instance):
        """Inicializa la clase Mainwindow

        Args:
            main_window_instance (Class): Establece una variable de tipo MainWindow que
            ayuda poder llamar a los metodos correspondientes (rojo, amarillo, azul, verde)
            """
        super().__init__()
        self.main_window = main_window_instance
        
    signal_azul = pyqtSignal()
    signal_rojo = pyqtSignal()
    signal_verde = pyqtSignal()
    signal_amarillo = pyqtSignal()
    signal_apagado=pyqtSignal()
        
    '''Implementacion de signals'''
    def signals(self, x):
        
        if x == 6:
            return self.signal_azul.emit()
        elif x == 7:
            return self.signal_rojo.emit()
        elif x == 8:
            
            return self.signal_verde.emit()
        elif x == 9:
            return self.signal_amarillo.emit()
        elif x == 0:
            return self.signal_apagado.emit()
        
        
    finished = pyqtSignal()  # Señal que indica el final del juego
    
    
    def run(self):
        
        if not hasattr(inspect, 'getargspec'):
            inspect.getargspec = inspect.getfullargspec

        board = pyfirmata.Arduino('COM5')
        it = pyfirmata.util.Iterator(board)
        it.start()

       
        
        '''Melodias con duracion'''
        melodia_error = [262, 196, 196, 220, 196, 1000, 247, 262]
        melodia_x=[262, 262,196, 196 ]
        melodia_bienvenida = [415.30, 392, 369.99, 349.23, 329.63, 311.13, 293.66, 277.18, 261.63]
        duracionNotas = [4000, 8000, 8000, 4000, 4000, 4000, 4000, 4000]
        duracionNotas_2 = [3000, 7000, 3000, 5000, 3000, 2000, 9000, 2000]

        '''Botones'''
        bt1 = board.get_pin('d:2:i' )
        bt2 = board.get_pin('d:3:i' )
        bt3 = board.get_pin('d:4:i' )
        bt4 = board.get_pin('d:5:i' )

        '''LEDS'''
        
        azul = board.get_pin('d:6:o')
        rojo = board.get_pin('d:7:o')
        verde = board.get_pin('d:8:o')
        amarillo= board.get_pin('d:9:o')

        '''Buzzer y melodias'''
        buzzer = board.get_pin('d:10:p' )

        def pusheo():
            buzzer.write(1)
            time.sleep(1/10)
            buzzer.write(0)

        def bienvenida():
            for i in range(8):
                duracionNota = 1000/duracionNotas[i]
                buzzer.write(1000/melodia_error[i])
                time.sleep(duracionNota)
                pausaEntreNotas = duracionNota * 1.30
                buzzer.write(0)
                time.sleep(pausaEntreNotas) 

        def error():
            for i in range(8):
                duracionNota = 1000/duracionNotas_2[i]
                buzzer.write(1000/melodia_error[i])
                time.sleep(duracionNota)
                pausaEntreNotas = duracionNota * 1.30
                buzzer.write(0)
                time.sleep(pausaEntreNotas)

        def paso_nivel():
            for i in range(4):
                buzzer.write(1000/melodia_error[i])
                time.sleep(1/10)
                pausaEntreNotas = 1/10 * 1.30
                buzzer.write(0)
                time.sleep(pausaEntreNotas)
                
                
        '''Variables de ayuda'''
        niveles=0
        x=0
        y=0
        pos_orden=-1
        combinaciones=[]


        '''Secuencia de inicio'''

        def inicio():
            print('Bienvenido \n Inicio')

            bienvenida()
            for i in range(6,10):
                board.digital[i].write(1)
                time.sleep(1/10)
                board.digital[i].write(0)
                
            #buz.melodia_bienvenida()

        '''Generar secuencia aleatoria'''
        def generar():
            x= rand.randint(6,9)
            combinaciones.append(x)
            return combinaciones

        def mostrar():
            secuencia=generar()
            for i in secuencia:
                board.digital[i].write(1)
                self.signals(i)
                time.sleep(1)
                board.digital[i].write(0)
                self.signals(0)
            print(secuencia)


            '''Principal -Loop-'''
        while True:            
            if niveles == 0:
                inicio()
                niveles+=1
                        
            else:
                pos_orden= -1
                time.sleep(1)
                mostrar()
                while True:
                            
                    while True:
                        boton1= bt1.read()
                        boton2= bt2.read()
                        boton3= bt3.read()
                        boton4= bt4.read()
                            
                        if boton1 == 1:
                            pusheo()
                            print('bton 1')
                            azul.write(1)
                            self.signals(6)
                            time.sleep(1)
                            azul.write(0)
                            self.signals(0)
                            estado=6
                            print(6)
                            pos_orden+=1
                                    
                            break
                                
                        elif boton2 == 1:
                            pusheo()
                            print('bton 2')
                            rojo.write(1)
                            self.signals(7)
                            time.sleep(1)
                            rojo.write(0)
                            self.signals(0)
                            estado=7
                            print(7)
                            pos_orden+=1
                            break
                            
                        elif boton3 == 1:
                            pusheo()
                            print('bton 3')
                            verde.write(1)
                            self.signals(8)
                            time.sleep(1)
                            verde.write(0)
                            self.signals(0)
                            estado=8
                            print(8)
                            pos_orden+=1
                            break
                                
                        elif boton4 == 1:
                            pusheo()
                            print('bton 4')
                            amarillo.write(1)
                            self.signals(9)
                            time.sleep(1)
                            amarillo.write(0)
                            self.signals(0)
                            estado=9
                            print(9)
                            pos_orden+=1
                            break
                        
                            
                    if  combinaciones[pos_orden] == estado:
                        #Secuencia buena:
                        print('OK')
                        y+=1
                        
                        if len(combinaciones) == y:
                            y=0
                            break
                    else:
                        error()
                        y=1
                        break
                if y != 1:            
                    paso_nivel()
                else:
                    break


        self.finished.emit()
        


 
 

class Instrucciones(QMainWindow, Ui_Dialog):
    def __init__(self, *parent, **flags) -> None:
        super().__init__(*parent, **flags)
        self.setupUi(self)



if __name__ == "__main__":
    
    app = QtWidgets.QApplication(sys.argv)
    window = Principal()
    window.show()
    sys.exit(app.exec())