from Ui_Interfaz2 import *
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import sys
import socket
from PyQt6.QtWidgets import QApplication, QLCDNumber, QVBoxLayout, QWidget


class ThreadSocket(QThread):
    global connected
    signal_message = pyqtSignal(str)
    
    def __init__(self, host, port):
        global connected
        super().__init__()
        server.connect((host, port))
        connected = True

    def run(self):
        global connected
        try:
            while connected:
                message = server.recv(BUFFER_SIZE)
                if message:
                    self.signal_message.emit(message.decode("utf-8"))
                else:
                    self.signal_message.emit("<!!disconected!!>")
                    break
                
        except ...:
            self.signal_message.emit("<!!error!!>")
        finally:
            server.close()
            connected = False
        
    def stop(self):
        global connected
        connected = False
        self.wait()


class Principal(QMainWindow,Ui_MainWindow):
    
    def __init__(self, *parent, **flags) -> None:
        super().__init__(*parent, **flags)
        self.setupUi(self)
        self.coneccion = None
        self.pushButton.clicked.connect(self.conec)
        self.pushButton_2.clicked.connect(self.mensaje_saliente)
        self.mensage_entrante
        
    def mensaje_saliente(self):
        str = "0"
        if str != "" and connected:
            server.send(bytes(str, 'utf-8'))
            self.mensage_entrante(str)
    
    def conec(self):
        user = 'EMPRESA'
        host='127.0.0.1'
        port = 65535        
        self.coneccion = ThreadSocket(host, int(port))
        self.coneccion.signal_message.connect(self.mensage_entrante)
        self.coneccion.start()
        self.datos.clear()
        self.mensage_entrante('Conexion')
        print('conectado')   

    def mensage_entrante(self, mensaje):
        self.datos.clear()
        posiciondos = mensaje.find('>')
        datos = mensaje[(posiciondos + 1)::]
        self.datos.setPlainText(self.datos.toPlainText() + "Nuevos datos: " + datos)
        
        esfera = datos.find('esfera')
        cubo = datos.find('cubo')
        otros = datos.find('otros')
        
        if esfera != -1:
            nesfera = datos[(esfera + 9):datos.find(',')]
            print(f'esferas: {nesfera}')
            self.lcd_esfera.display(int(nesfera))
            
        if cubo != -1:
            ncubo = datos[(cubo + 7):datos.find(', otro')]
            print(f'cubos: {ncubo}')
            self.lcd_cubos.display(int(ncubo))
            
        
        
    
        
    
if __name__ == "__main__":
    BUFFER_SIZE = 1024 
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connected = False
    app = QtWidgets.QApplication(sys.argv)
    window = Principal()
    window.show()
    sys.exit(app.exec())
