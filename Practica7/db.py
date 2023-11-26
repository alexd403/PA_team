from pymongo import MongoClient

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
