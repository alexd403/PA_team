 # * Librerias esenciales para el uso de las comunicaciones tpc
import socket
# * El uso de la libreria (threading) permite el uso de hilos que se ejecutan en paralelo
import threading


username = input('Introduce un nombre de usuario: ')
host = '127.0.0.1'  # !localhost- Donde se ecuntra el loopback
port = 5003 # ! Puerto el cual se establecera la comunicacion
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((host, port))

def recive_messages():
    while True:
        try:
            mensaje = client.recv(1024).decode('utf-8')
            
            if mensaje == '@username:':
                #El decode es necesario ya que estamos haciendo uso de la terminal
                client.send(username.encode('utf-8'))
            else:
                print(mensaje)
        except: 
            print('Something Failed):')
            client.close()
            break
        
def writing():
    while True:
        x=input('')
        client.send(f'{username}: {x}'.encode('utf-8'),)
        
#! Necesitamos dos hilos para poder hacer correres las dos funciones en paralelo
recive = threading.Thread(target=recive_messages).start()
    
write =threading.Thread(target=writing).start()
