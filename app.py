import flask
from flask import Flask, render_template, redirect, request
from waitress import serve
from forms.user import RegisterForm, LoginForm
from flask_restful import Api
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from data.users import User
from data.posts import Post
from data.user_resource import UsersResource, UsersListResource
from data.post_resource import PostsResource, PostsListResource
import requests

# Инициализация веб приложения
app = Flask(__name__)
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'test_key'  # Потом изменить!!!


@app.route('/')
def index():
    # Главная страница

    posts = requests.get(f'http://localhost:8080/api/posts').json()
    name = []
    for i in reversed(posts['posts']):
        name.append(requests.get(f'http://localhost:8080/api/users/{i["user_id"]}').json()['user']["login"])

    print(posts)
    return render_template('index.html', title='Главная страница', get_nav=True, current_user=current_user,
                           args=reversed(posts['posts']), name=name)


@app.route('/u/<s>')
def uuposts(s):
    posts = requests.get(f'http://localhost:8080/api/posts').json()
    name = []
    for i in reversed(posts['posts']):
        name.append(requests.get(f'http://localhost:8080/api/users/{i["user_id"]}').json()['user']["login"])

    print(posts)
    return render_template('index.html', user_id=posts['posts']['user_id'], title='Главная страница', get_nav=True, s=s,
                           args=reversed(posts['posts']), name=name)


@app.route('/register', methods=['GET', 'POST'])
def register():
    # форма регистрации
    form = RegisterForm()
    heading_h1 = 'Регистрация'
    title = 'Регистрация'
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title=title, get_nav=False,
                                   get_password=True, heading_h1=heading_h1,
                                   form=form, message='Пароли не совпадают', footer_register=True)
        response = requests.get('http://localhost:8080/api/users').json()
        logins, emails = False, False
        for user in response['users']:
            if form.login.data == user['login']:
                logins = True
                break
            elif form.email.data == user['email']:
                emails = True
                break
        if logins:
            return render_template('register.html', title=title, get_nav=False,
                                   get_password=True, heading_h1=heading_h1,
                                   form=form, message='Такой логин уже занят!', footer_register=True)
        if emails:
            return render_template('register.html', title=title, get_nav=False,
                                   get_password=True, heading_h1=heading_h1,
                                   form=form, message='Такая почта уже занята!', footer_register=True)
        requests.post('http://127.0.0.1:8080/api/users', json={'login': form.login.data,
                                                               'email': form.email.data,
                                                               'surname': form.surname.data,
                                                               'name': form.surname.data,
                                                               'password': form.password.data})
        return redirect('/login')
    return render_template('register.html', title=title, get_nav=False, heading_h1=heading_h1,
                           get_password=True, form=form, footer_register=True)





@app.route('/login', methods=['GET', 'POST'])
def login():
    # форма входа
    form = LoginForm()
    heading_h1 = "Вход"
    title = 'Вход'
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if "@" in form.login_email.data:
            user = db_sess.query(User).filter(User.email.like(form.login_email.data)).first()
        else:
            user = db_sess.query(User).filter(User.login.like(form.login_email.data)).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            db_sess.close()
            return redirect('/menu')
        db_sess.close()
        return render_template('login.html',
                               get_nav=False,
                               title=title,
                               heading_h1=heading_h1,
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title=title, heading_h1=heading_h1, get_nav=False, form=form)


@app.route('/menu')
@login_required
def menu():
    title = 'Меню'
    heading_h1 = "Меню"
    return render_template('menu.html', title=title, user=current_user, get_nav=True, heading_h1=heading_h1)


@app.route('/addpost', methods=['GET', 'POST'])
@login_required
def addpost():
    if flask.request.method =='GET':
        return render_template('addpost.html')
    elif flask.request.method == "POST":
        print(flask.request.values.get('img'), flask.request.values.get('tags'))
        requests.post('http://127.0.0.1:8080/api/posts', json={'title': flask.request.values.get('title'),
                                                               'content': flask.request.values.get('content'),
                                                               'img': flask.request.values.get('img'),
                                                               'tags': flask.request.values.get('tags'),
                                                               'user': current_user.name,
                                                               'user_id': current_user.id})
        return redirect(f'/')


@app.route('/p/<s>')
def ppost(s):
    posts = requests.get(f'http://localhost:8080/api/posts/{s}').json()
    print(posts["post"]["user_id"])
    name = requests.get(f'http://localhost:8080/api/users/{posts["post"]["user_id"]}').json()
    print(posts, name)
    print(name["user"]["login"])
    return render_template('postt.html', a=posts['post'], username=name["user"]["login"])



@app.route('/change_data', methods=['GET', 'POST'])
def change_data():
    title = 'Изменить данные аккаунта'
    heading_h1 = "Изменить данные аккаунта"
    form = RegisterForm()
    form.submit.label.text = 'Изменить'
    if form.validate_on_submit() or request.method == 'POST':
        response = requests.get('http://localhost:8080/api/users').json()
        logins, emails = False, False
        for user in response['users']:
            if user['id'] == current_user.id:
                continue
            elif user['email'] == form.email.data:
                emails = True
                break
            elif user['login'] == form.login.data:
                logins = True
                break
        if logins:
            user = requests.get(f'http://loaclhost:8080/api/users/{current_user.id}').json()['user']
            form.login.data = user['login']
            form.email.data = user['email']
            form.surname.data = user['surname']
            form.name.data = user['name']
            return render_template('register.html', title=title, get_nav=False,
                                   get_password=False, heading_h1=heading_h1,
                                   form=form, message='Такой логин уже занят!', footer_register=False)
        if emails:
            user = requests.get(f'http://loaclhost:8080/api/users/{current_user.id}').json()['user']
            form.login.data = user['login']
            form.email.data = user['email']
            form.surname.data = user['surname']
            form.name.data = user['name']
            return render_template('register.html', title=title, get_nav=False,
                                   get_password=False, heading_h1=heading_h1,
                                   form=form, message='Такая почта уже занята!', footer_register=False)
        response = requests.put(f'http://127.0.0.1:8080/api/users/{current_user.id}',
                                json={'name': form.name.data, 'surname': form.surname.data, 'email': form.email.data,
                                      'login': form.login.data})
        return response.json()  # Фронтендер, переделай так, чтоб красиво показать пользователю, что все ОК
    user = requests.get(f'http://localhost:8080/api/users/{current_user.id}').json()['user']
    form.login.data = user['login']
    form.email.data = user['email']
    form.surname.data = user['surname']
    form.name.data = user['name']
    return render_template('register.html', title=title, get_nav=False, heading_h1=heading_h1,
                           get_password=False, form=form, footer_register=False)


@app.route('/logout')
@login_required
def logout():
    # функция для выхода из аккаунта
    logout_user()
    return redirect('/')


@login_manager.user_loader
def load_user(user_id):
    # загружает пользователя
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    db_sess.close()
    return user


def main():
    # запуск приложения
    db_session.global_init('db/db.sqlite')
    api.add_resource(UsersResource, '/api/users/<int:user_id>')
    api.add_resource(UsersListResource, '/api/users')
    api.add_resource(PostsResource, '/api/posts/<int:post_id>')
    api.add_resource(PostsListResource, '/api/posts')
    app.run(host='127.0.0.1', port=8080, debug=True)
    # serve(app, host='127.0.0.1', port=8080)  # Потом раскомментировать перед выпуском в мир


if __name__ == '__main__':
    main()

