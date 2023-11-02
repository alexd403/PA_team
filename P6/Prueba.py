from PyQt6 import QtCore,QtGui,QtWidgets
from Ui_Simon import *
from Ui_PrincipalSimon import *
from Ui_Instrucciones import *
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QWidget, QApplication
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
        
    def jugar(self):
        self.ventana.show()
        self.close()
    
    def instrucciones(self):
        self.instruc.show()

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *parent, **flags) -> None:
        super().__init__(*parent, **flags)
        self.setupUi(self)

        self.Rojobtn.clicked.connect(self.rojo)
        self.Amarillobtn.clicked.connect(self.amarillo)
        self.Azulbtn.clicked.connect(self.azul)
        self.Verdebtn.clicked.connect(self.verde)
        self.Apagarbtn.clicked.connect(self.apagado)
        self.Regresarbtn.clicked.connect(self.regresar)

    def rojo(self):
        for Qlabel in window.findChildren(QWidget):
            if Qlabel is not self.Rojo:
                Qlabel.lower()
        self.Rojo.raise_()

    def amarillo(self):
        for Qlabel in window.findChildren(QWidget):
            if Qlabel is not self.Amarillo:
                Qlabel.lower()
        self.Amarillo.raise_()
    
    def azul(self):
        for Qlabel in window.findChildren(QWidget):
            if Qlabel is not self.Azul:
                Qlabel.lower()
        self.Azul.raise_()

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

    def regresar(self):
        window.show()
        self.close()

class Instrucciones(QMainWindow, Ui_Dialog):
    def __init__(self, *parent, **flags) -> None:
        super().__init__(*parent, **flags)
        self.setupUi(self)

if __name__ == "__main__":
        if not hasattr(inspect, 'getargspec'):
            inspect.getargspec = inspect.getfullargspec

        board = pyfirmata.Arduino('COM6')

        it = pyfirmata.util.Iterator(board)
        it.start()


        '''Botones'''
        bt1 = board.get_pin('d:10:i' )
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

        melodia_error = [262, 196, 196, 220, 196, 1000, 247, 262]
        melodia_x=[262, 262,196, 196 ]
        melodia_bienvenida = [415.30, 392, 369.99, 349.23, 329.63, 311.13, 293.66, 277.18, 261.63]
        duracionNotas = [4000, 8000, 8000, 4000, 4000, 4000, 4000, 4000]
        duracionNotas_2 = [3000, 7000, 3000, 5000, 3000, 2000, 9000, 2000]

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
                time.sleep(1)
                board.digital[i].write(0)
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
                            time.sleep(1)
                            azul.write(0)
                            estado=6
                            print(6)
                            pos_orden+=1
                            
                            break
                        
                        elif boton2 == 1:
                            pusheo()
                            print('bton 2')
                            rojo.write(1)
                            time.sleep(1)
                            rojo.write(0)
                            estado=7
                            print(7)
                            pos_orden+=1
                            break
                        
                        elif boton3 == 1:
                            pusheo()
                            print('bton 3')
                            verde.write(1)
                            time.sleep(1)
                            verde.write(0)
                            estado=8
                            print(8)
                            pos_orden+=1
                            break
                        
                        elif boton4 == 1:
                            pusheo()
                            print('bton 4')
                            amarillo.write(1)
                            time.sleep(1)
                            amarillo.write(0)
                            estado=9
                            print(9)
                            pos_orden+=1
                            break
                        else:
                            pass
                    
                    if  combinaciones[pos_orden] == estado:
                        #Secuencia buena:
                        print('OK')
                        y+=1
                        if len(combinaciones) == y:
                            y=0
                            break
                    else:
                        error()
                        exit()
            paso_nivel()    
            
    app = QtWidgets.QApplication(sys.argv)
    window = Principal()
    window.show()
    sys.exit(app.exec())