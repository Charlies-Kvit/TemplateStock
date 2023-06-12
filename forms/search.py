from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class AppSearch(FlaskForm):
    search = StringField('Поиск')
    submit = SubmitField('Искать')
