from Ui_Menu import *
from Ui_Registro import *
from Ui_chat import *
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6 import QtWidgets,  QtGui
from PyQt6.QtCore import *
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtGui import QImage
import threading
import socket
import cv2
import sys
import db
import correo
from PyQt6.uic import loadUi
 
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
class Chat(QMainWindow, Ui_Chat, QThread):
    
    
    
    def __init__(self) -> None:
        
        super().__init__()
        self.setupUi(self)
        self.coneccion = None
        # Conexion con funciones al oprimir los botones
        self.Enviar_btn.clicked.connect(self.Enviar)
        #self.listWidget.currentItemChanged.connect(self.actualizarLabel)#Conexion del widget de lista 
        #self.listWidget.itemClicked.connect(self.reiniciarArchivo)      
        
    # def actualizarLabel(self):
    #     # Obtener el texto del elemento seleccionado
    #     texto_seleccionado = self.listWidget.currentItem().text()
    #     # Mostrar el texto en el QLabel
    #     self.label_4.setText(f" {texto_seleccionado}")
    #     ##
    # #def reiniciarArchivo(self):#Funcion de prueba
       # open("Dialogo.txt", "w")

    def Enviar(self):
        #Mensaje que debe de llegar la clase S
        dialogo=self.Insertar_Texto1.toPlainText()
    
        print(dialogo)
        
        if dialogo != "" and connected:
            server.send(bytes(dialogo, 'utf-8'))
            self.Insertar_Texto1.clear()
            self.mensage_entrante("<Tú> " + dialogo + '\n')
        
                
    #def reset_txt(self):#Presuntamente se encarga de reiniciar el txt cada que se seleccione a una nueva persona en el chat 
        #pass
    
                
    def mensage_entrante(self, mensaje):
        self.plainTextEdit.setPlainText(self.plainTextEdit.toPlainText() + mensaje)
    
    def setPhoto(self, img_user):
        image = db.busqueda_img(img_user)
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        imagen = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format.Format_RGB888)
        imagen = imagen.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio)
        self.img_lbl.setPixmap(QtGui.QPixmap.fromImage(imagen))


    
class Menu(QMainWindow, Ui_Menu):
    signal_mensaje = pyqtSignal(str)
    def __init__(self, *parent, **flags) -> None:
        super().__init__(*parent, **flags)
        self.setupUi(self)
        self.user=""
        self.password=""
        self.ip=""
        self.port=""
        
        self.regis=Registro()
        self.chatp=Chat()
        
        self.ingresar_btn.clicked.connect(self.ingreso)
        self.ingresar_btn.clicked.connect(self.showDialog)
        self.cuenta_btn.clicked.connect(self.registro)
    
       
    def ingreso(self):
        self.user=self.usuario_txe.toPlainText()
        self.password=self.contra_txe.text()
        self.ip=self.ip_txe.toPlainText()
        self.port=self.port_txe.toPlainText()
        
        x , y = db.find(self.user)
        
        print(x,y)
        if self.user == x and self.password == y:
            print("Acceso")
            self.chatp.show()
            self.chatp.setPhoto(self.user)
            self.close()
            self.coneccion = ThreadSocket(self.ip, int(self.port))
            self.coneccion.signal_message.connect(self.mensage_entrante)
            self.coneccion.start()
            
        else:
            self.incorrecto()
            
    def showDialog(self):
        
        print(self.ip, self.user, self.port)
            
        if self.ip and not self.ip.isspace() and self.port and self.port.isnumeric():
            #self.coneccion = ThreadSocket(self.ip, int(self.port))
            self.coneccion.signal_message.connect(self.mensage_entrante)
            
    def mensage_entrante(self, mensaje):
        #self.chatp.self.chat.setPlainText(self.chatp.self.chat.toPlainText() + mensaje)
        pass
    
    def incorrecto(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Ingreso incorrecto.")
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText("Datos de ingreso incorrectos")
        msg.setInformativeText("Por favor verifica tu usuario o contraseña.")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

    def registro(self):
        self.regis.show()


class Registro(QMainWindow, Ui_Registro):
    def __init__(self,*parent, **flags) -> None:
        super().__init__(*parent, **flags)
        self.setupUi(self)
        self.user = None
        self.imagen = None
        self.registrar_btn.clicked.connect(self.registo)
        self.imagen_btn.clicked.connect(self.cargarImagen)
        #self.label_4.setText("Conectado")
   
    
    def registo(self):
        email=self.correo_txe.toPlainText()
        self.user=self.usue_txe.toPlainText()
        # ! Esta variable debe ser de entorno por seguridad
        password=self.contras_txe.toPlainText()
        
        x , y = db.find(self.user)

        if x and y == 1:
                
            db.database(self.user, email, password)
            correo.send_email(email,self.user)
            imagen_usuario= self.imagen
            # ! Corregir a la hora de no subir imagen
            try:
                db.imagen(self.user, imagen_usuario)
            except:
                pass
            
        else:
            self.incorrecto()

        self.close()

    def cargarImagen(self):
        
        try:
            global filename
            filename = QFileDialog.getOpenFileName(filter="Image (*.*)")[0]
            self.imagen = cv2.imread(filename)
            
            self.setPhoto(self.imagen)
            
        except:
            pass
        
    def incorrecto(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Usuario ya registrado")
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText("Inicia sesion con tu nombre de usuario")
        msg.setInformativeText("Si olvidaste tu contraseña, contactenos a servermexicoupiitos@gmail.com.")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

    def setPhoto(self,image):
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        imagen = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format.Format_RGB888)
        imagen = imagen.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio)
        self.imagen_lbl.setPixmap(QtGui.QPixmap.fromImage(imagen))
    
   
    




    
 # Agregue su lógica para manejar el mensaje según sea necesari
if __name__ == "__main__":
    BUFFER_SIZE = 1024  # Usamos un número pequeño para tener una respuesta rápida
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connected = False
    app = QtWidgets.QApplication(sys.argv)
    window = Menu()
    window.show()
    sys.exit(app.exec())