from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class AddPost(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    content = StringField('Описание', validators=[DataRequired()])
    image = StringField('Изображение (ссылка)')
    tags = StringField('Тэги (через ;)')
