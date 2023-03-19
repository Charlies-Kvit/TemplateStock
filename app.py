from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test_key'  # Потом изменить!!!


@app.route('/')
def index():
    return "<h1>Главная страница - Марта, ты сможешь!!!</h1>"


@app.route('/register')
def register():
    pass


@app.route('/login')
def login():
    pass


def main():
    app.run(host='127.0.0.1', port=8080)


if __name__ == '__main__':
    main()
