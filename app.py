from flask import Flask, render_template, redirect
from forms.user import RegisterForm, LoginForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from data.users import User

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'test_key'  # Потом изменить!!!


@app.route('/')
def index():
    return "<h1>Главная страница - Марта, ты сможешь!!!</h1>"


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    db_sess = db_session.create_session()
    title = 'Регистрация'
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title=title, form=form, message='Пароли не совпадают')
        logins = db_sess.query(User).filter(User.login.like(form.login.data)).first()
        if logins:
            return render_template('register.html', title=title, form=form, message='Такой логин уже занят!')
        emails = db_sess.query(User).filter(User.email.like(form.email.data)).first()
        if emails:
            return render_template('register.html', title=title, form=form, message='Такая почта уже занята!')
        user = User(
            login=form.login.data,
            email=form.email.data,
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        db_sess.close()
        return redirect('/login')
    return render_template('register.html', title=title, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
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
            return redirect('/')
        return render_template('login.html',
                               title=title,
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title=title, form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def main():
    db_session.global_init('db/db.sqlite')
    app.run(host='127.0.0.1', port=8080)


if __name__ == '__main__':
    main()
