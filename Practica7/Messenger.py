from Ui_Menu import *
from Ui_Registro import *
from Ui_chat import *
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6 import QtWidgets,  QtGui
from PyQt6.QtCore import *
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtGui import QImage
import cv2
import sys
import db
import correo 
 

class Menu(QMainWindow, Ui_Menu):
    def __init__(self, *parent, **flags) -> None:
        super().__init__(*parent, **flags)
        self.setupUi(self)

        self.chat=Chat()
        self.regis=Registro()

        self.ingresar_btn.clicked.connect(self.ingreso)
        self.cuenta_btn.clicked.connect(self.registro)
        
    def ingreso(self):
        user=self.usuario_txe.toPlainText()
        password=self.contra_txe.text()
        ip=self.ip_txe.toPlainText()
        port=self.port_txe.toPlainText()
        
        x , y = db.find(user)
        
        print(x,y)
        if user == x and password == y:
            print("Acceso")
            self.chat.show()
            self.close()
            
        else:
            self.incorrecto()
    
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
    def __init__(self, *parent, **flags) -> None:
        super().__init__(*parent, **flags)
        self.setupUi(self)

        self.registrar_btn.clicked.connect(self.registo)
        self.imagen_btn.clicked.connect(self.cargarImagen)

    def registo(self):
        email=self.correo_txe.toPlainText()
        user=self.usue_txe.toPlainText()
        password=self.contras_txe.toPlainText()
        
        x , y = db.find(user)
        
        if x and y == 1:
            
            db.database(user, email, password)
            correo.send_email(email,user)
            
        else:
            self.incorrecto()
            
        self.close()

    def cargarImagen(self):
        try:
            global filename
            filename = QFileDialog.getOpenFileName(filter="Image (*.*)")[0]
            imagen = cv2.imread(filename)
            self.setPhoto(imagen)
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
    
class Chat(QMainWindow, Ui_Chat):
    def __init__(self, *parent, **flags) -> None:
        super().__init__(*parent, **flags)
        self.setupUi(self)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Menu()
    window.show()
    sys.exit(app.exec())