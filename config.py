from key_generator import secret_key_generator

HOST = '127.0.0.1'
DEBUG = False
DATABASE = 'db/db.sqlite'
PORT = 8080
SECRET_KEY = secret_key_generator(100)
API_KEY = secret_key_generator(100)
