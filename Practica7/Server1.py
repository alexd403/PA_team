 # * Librerias esenciales para el uso de las comunicaciones tpc
import socket
# * El uso de la libreria (threading) permite el uso de hilos que se ejecutan en paralelo
import threading

host = '127.0.0.1' # !localhost- Donde se ecuntra el loopback
port = 5003# ! Puerto el cual se establecera la comunicacion /5003

# ? Creacion del socket que se encargara de establecer la comunicacion
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

'''
# * AF_INET: Indica que se hara uso de un socket de tipo internet
# * SOCK_STREAM: Indica comunicacion TCP 
'''
# Pase los datos de coneccion al socket 
server.bind((host, port))

# * Escucha a las conexiones.
server.listen()
print(f"Server is running on {host} : {port} ")

# * En el programa se podran conectar varios usuarios
clients= []
users= []

def broadcast(mensaje, _client): #Encargado de hacer llegar los mensajes a cada usuario conectado
    #Enviamos el mensaje a todos los usuarios menos al que lo emitio
    print('He llegado a la emision')
    for client in clients:
        try:
            if client != _client:
                client.send(mensaje)
        except:
            pass
            


def handle_messages(client): #Encargado de hacer el manejo de mensajes
    while True:
        try:
            #Recive mensajes con una cantidad maxima de 1024 bytes
            mensaje = client.recv(1024)
            broadcast(mensaje, client)
        except:
            #En caso de que ocurra un error mandamos el siguiente mensaje
            print ('Error')
            pos = clients.index(client)
            username = users[pos]
            #Para mander mensajes necesitamos hacer una codificacion utf-8 para convertir 
            #los strings en bytes
            broadcast(f'Chatbot: {username} disconnected'.encode('utf-8'), client)
            clients.remove(client)
            users.remove(username)
            print ('Client removed')
            server.close()
            break
        
def recive_connections():
    while True:
        try:
            client, address =server.accept() #* Esta funcion me retorna dos valores que son la ip y el port
            client.send(f'@username:'.encode('utf-8'))
            user= client.recv(1024).decode('utf-8')
        except:
            break
        
        #! Agregamos el cliente y el nombre de usuario que se vayan conectando
        clients.append(client)
        users.append(user)
        
        print(f'User: {user} is connected with address: {str(address)}')
        
        #* Mensaje dirigido a todos los clientes que se encuntren conectados.
        mensaje= f'{user} is connected'.encode('utf-8')
        broadcast(mensaje, client)
        
        #! Mensaje dirigido al usuario conectado
        client.send('You are connected'.encode('utf-8'))
      
        #! Creacion de los hilos paralelos
        thread = threading.Thread(target=handle_messages, args=(client,)).start()

recive_connections()
