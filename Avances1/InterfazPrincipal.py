from Ui_Interfaz1 import *
import numpy as np
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QDialog
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtCore import pyqtSlot
import cv2
import sys
import pyfirmata
import time
import inspect
import steplib
import socket
import datetime
from ultralytics import YOLO

class ThreadSocket(QThread):
    global connected
    signal_message = pyqtSignal(str)
    
    def __init__(self, host, port):
        global connected
        super().__init__()
        server.connect(('localhost', port))
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



        self.Work = Work(self)
        self.Serial=Serial(self)
        self.pushButton_2.clicked.connect(self.Enviar_datos)
        self.pushButton_3.clicked.connect(self.inicio)
        self.Work.esfera_s.connect(self.esferaa)
        self.Work.cubo_s.connect(self.cuboo)
        #self.Work.datos.connect(self.obtener_datos)
        self.x = 0
        self.y = 0
        self.Work.Imageupd.connect(self.Imageupd_slot)
        #self.Work.Emergencia.connect(self.paro)
        
    def conteo(self):
        self.label_2.setText(str(int(self.x)))
        self.label_3.setText(str(int(self.y)))
        z=self.x + self.y
        self.label_4.setText(str(int(z)))
        
        
    def esferaa(self):
        self.x+=1
        print('recibio señal')
        angle=65
        servo1.write(angle)
        time.sleep(0.5)
        buzzer.write(1)
        time.sleep(1/10)
        buzzer.write(0)
        print("Se movio")
        print(self.x)
        self.conteo()
        
    def cuboo(self):
        self.y+=1
        print('recibio señal')
        angle=0
        servo1.write(angle)
        time.sleep(0.5)
        buzzer.write(1)
        time.sleep(1/10)
        buzzer.write(0)
        print("Se movio") 
        print(self.y)
        self.conteo()
         
    def inicio(self):
        self.Work.start()
        self.Serial.start()
        
    @pyqtSlot(QImage)    #Funcion que abre camara en label
    def Imageupd_slot(self, Image):
        self.label.setPixmap(QPixmap.fromImage(Image))
        
    @pyqtSlot(int, int)
    def obtener_datos(self, cubo, esferas):
        self.x = str(cubo)
        self.y = str(esferas)
        
    def Enviar_datos(self):
        server.send(bytes(f'esfera = {self.y}, cubo = {self.x}, otro = {self.x + self.y}', 'utf-8'))
       
        print('se enviaron los datos')

    def paro(self):  #Mensaje que aparece al tener un paro de emergencia
        msg = QMessageBox(self)
        msg.setWindowTitle("Advertencia")
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setText("PARO DE EMERGENCIA")
        msg.setInformativeText(f"Se ha activado un paro de emergencia, pr favor verifica.")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)

    
    
class Serial(QThread):
    
    def __init__(self, main_window_instance):
        """Inicializa la clase Mainwindow

        Args:
            main_window_instance (Class): Establece una variable de tipo MainWindow que
            ayuda poder llamar a los metodos correspondientes.
            """
        super().__init__()
        self.main_window = main_window_instance
        self.coneccion = None
       
        
    datos = pyqtSignal(int, int)   
    
    #Hilo que conecta Boton de emergencia
    #Emergencia=pyqtSignal()
    
   
                   
    
    def run(self):
        try:
            user = 'EMPRESA'
            port = 65535        
            self.coneccion = ThreadSocket('localhost', int(port))
            self.coneccion.start()
        except:
            pass
        print('conectado')   
        
         # Indica que un servo se movio
        def mov():
            buzzer.write(1)
            time.sleep(1/10)
            buzzer.write(0)
            print("Se movio")

        #Variables de apoyo
        cubo=0
        esferas=0
        general=0

        while True:
            #Motor corriendo
            motor.step(4096)

            angle=0

        
            print(btn.read())
            
               
            if btn.read() == False:
                print("paroooo")
                motor.off()
                #self.Emergencia.emit()
                buzzer.write(1)
                time.sleep(2)
                buzzer.write(0)
                break
        
              
class Work(QThread):
    
    Imageupd = pyqtSignal(QImage)
    
    def __init__(self, main_window_instance):
        super().__init__()
        self.main_window = main_window_instance
        self.hilo_corriendo = True
        self.model = YOLO("best.pt")
        
        self.names = self.model.names
        self.CONFIDENCE_THRESHOLD = 0.6
        self.GREEN = (0, 255, 0)
        self.BLUE = (85, 100, 235)
        #Deteccion de objetos con señales.
        
    esfera_s=pyqtSignal()
    cubo_s=pyqtSignal()
        

    def run(self):
        

        cap = cv2.VideoCapture(0)
        while self.hilo_corriendo:
            start = datetime.datetime.now()
            ret, frame = cap.read()
            if ret:
                roi = frame[20:600, 80:350]
                xrmin, yrmin, xrmax, yrmax = 20, 20, 200, 350
                cv2.rectangle(roi, (xrmin, yrmin), (xrmax, yrmax), self.BLUE, 5)
                detections = self.model(roi, verbose=False)[0]

                for data in detections.boxes.data.tolist():
                    confidence = data[4]
                    if float(confidence) < self.CONFIDENCE_THRESHOLD:
                        continue

                    xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])
                    label = self.names[int(data[5])]
                    print(f"Detected: {label}")
                    
                    if label == 'cubo':
                        self.cubo_s.emit()
                        
                    
                    if label == 'esfera':
                        self.esfera_s.emit()
                        print('mando señaaaaal')
                    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), self.GREEN, 5)
                    cv2.putText(frame, label, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, self.GREEN, 2)

                # Convert and emit the frame for displaying in the GUI
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                flipped_image = cv2.flip(image, 1)
                qt_image = QImage(flipped_image.data, flipped_image.shape[1], flipped_image.shape[0], QImage.Format.Format_RGB888)
                resized_image = qt_image.scaled(481, 421, Qt.AspectRatioMode.KeepAspectRatio)
                self.Imageupd.emit(resized_image)

    

        
#* Este es exclusivo para realizar la comunicación
        
        
if __name__ == "__main__":
    
    BUFFER_SIZE = 1024  
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connected = False
    
    
    if not hasattr(inspect, 'getargspec'):
        inspect.getargspec = inspect.getfullargspec
                    
    board=pyfirmata.Arduino('COM6')

    it = pyfirmata.util.Iterator(board)
    it.start()

    ##Establecemos los pines##

    motor = steplib.Stepper(64, board, 8, 9, 10, 11)
    motor.set_speed(100)
    btn=board.get_pin('d:12:i') 
    buzzer=board.get_pin('d:6:p')
    servo1=board.get_pin('d:7:s') # s para servo

    app = QtWidgets.QApplication(sys.argv)
    window = Principal()
    window.show()
    sys.exit(app.exec())
        
