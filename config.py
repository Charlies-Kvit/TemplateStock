from key_generator import secret_key_generator

HOST = '127.0.0.1'
DEBUG = True
DATABASE = 'db/db.sqlite'
PORT = 8080
SECRET_KEY = secret_key_generator(100)
API_KEY = secret_key_generator(100)
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USERNAME = 'teamplatestock@gmail.com'
MAIL_PASSWORD = 'MGR9302124'
MAIL_USE_TLS = False
MAIL_USE_SSL = True
