from pymongo import MongoClient
import gridfs
import cv2
import base64
import numpy as np

mongo_uri = 'mongodb://localhost'
cliente = MongoClient(mongo_uri)
    
db = cliente['Users']
collections = db['Data']

def database(user, email, password ):
    
    user={'username': user, 'Correo': email, 'password': password}
    collections.insert_one(user)
    
def find(user):
    print(user)
    
    result = collections.find_one({'username': user})
    print(result)
    if result:
        return result['username'], result['password']
    
    else:
        return 1, 1
    
def imagen(user, imagen):
    # Codificación de la imagen a base64
    # !Necesita cambios para la codificacion del tipo de imagen
    _, buffer = cv2.imencode('.jpg', imagen)
    codificado = base64.b64encode(buffer)

    # Almacenamiento usando GridFS
    filename = user
    fs = gridfs.GridFS(db)
    id = fs.put(codificado, filename=filename)
    
    # Inserción de metadatos en la colección image
    db.Image.insert_one({'filename': filename, 'file_id': id})

def busqueda_img(user):
    # Acceso a GridFS
    fs = gridfs.GridFS(db)
    
    # Obtener el objeto GridOut correspondiente al archivo
    file_obj = fs.find_one({'filename': user})
    
    # Obtener el contenido codificado en base64
    codificado = file_obj.read()

    # Decodificar el contenido base64
    decoded = base64.b64decode(codificado)

    # Convertir los datos decodificados a un array NumPy
    buffer = np.frombuffer(decoded, dtype=np.uint8)

    # Decodificar el array NumPy con OpenCV
    imagen = cv2.imdecode(buffer, flags=cv2.IMREAD_UNCHANGED)

    return imagen

