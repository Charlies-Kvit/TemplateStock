from flask import Flask, render_template, redirect, request
from forms.user import RegisterForm, LoginForm
from flask_restful import Api
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from data.users import User
from data.user_resource import UsersResource, UsersListResource
import datetime

# Инициализация веб приложения
app = Flask(__name__)
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'test_key'  # Потом изменить!!!


@app.route('/')
def index():
    # Главная страница
    heading_h1 = "Меню"
    return render_template('index.html', title='Главная страница', get_nav=True, current_user=current_user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    # форма регистрации
    form = RegisterForm()
    db_sess = db_session.create_session()
    heading_h1 = 'Регистрация'
    title = 'Регистрация'
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title=title, get_nav=False,
                                   get_password=True, heading_h1=heading_h1,
                                   form=form, message='Пароли не совпадают')
        logins = db_sess.query(User).filter(User.login.like(form.login.data)).first()
        if logins:
            return render_template('register.html', title=title, get_nav=False,
                                   get_password=True, heading_h1=heading_h1,
                                   form=form, message='Такой логин уже занят!')
        emails = db_sess.query(User).filter(User.email.like(form.email.data)).first()
        if emails:
            return render_template('register.html', title=title, get_nav=False,
                                   get_password=True, heading_h1=heading_h1,
                                   form=form, message='Такая почта уже занята!')
        user = User(
            login=form.login.data,
            email=form.email.data,
            surname=form.surname.data,
            name=form.name.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        db_sess.close()
        return redirect('/login')
    db_sess.close()
    return render_template('register.html', title=title, get_nav=False, heading_h1=heading_h1,
                           get_password=True, form=form)


# @app.route('/u/<userid>')
# def userpage(userid):
#     return render_template('user_page.html')


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


@app.route('/change_data', methods=['GET', 'POST'])
def change_data():
    title = 'Изменить данные аккаунта'
    heading_h1 = "Изменить данные аккаунта"
    form = RegisterForm()
    form.submit.label.text = 'Изменить'
    if form.validate_on_submit() or request.method == 'POST':
        db_sess = db_session.create_session()
        logins = db_sess.query(User).filter(User.login.like(form.login.data), User.id != current_user.id).first()
        if logins:
            user = db_sess.query(User).filter(User.id == current_user.id).first()
            form.login.data = user.login
            form.email.data = user.email
            form.surname.data = user.surname
            form.name.data = user.name
            return render_template('register.html', title=title, get_nav=False,
                                   get_password=False, heading_h1=heading_h1,
                                   form=form, message='Такой логин уже занят!')
        emails = db_sess.query(User).filter(User.email.like(form.email.data), User.id != current_user.id).first()
        if emails:
            user = db_sess.query(User).filter(User.id == current_user.id).first()
            form.login.data = user.login
            form.email.data = user.email
            form.surname.data = user.surname
            form.name.data = user.name
            return render_template('register.html', title=title, get_nav=False,
                                   get_password=False, heading_h1=heading_h1,
                                   form=form, message='Такая почта уже занята!')
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        user.name = form.name.data
        user.surname = form.surname.data
        user.email = form.email.data
        user.login = form.login.data
        user.date_change = datetime.datetime.now()
        db_sess.commit()
        db_sess.close()
        return render_template("")
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    db_sess.close()
    form.login.data = user.login
    form.email.data = user.email
    form.surname.data = user.surname
    form.name.data = user.name
    return render_template('register.html', title=title, get_nav=False, heading_h1=heading_h1,
                           get_password=False, form=form)


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
    return db_sess.query(User).get(user_id)


def main():
    # запуск приложения
    db_session.global_init('db/db.sqlite')
    api.add_resource(UsersResource, '/api/users/<int:user_id>')
    api.add_resource(UsersListResource, '/api/users')
    app.run(host='127.0.0.1', port=8080, debug=True)


if __name__ == '__main__':
    main()

