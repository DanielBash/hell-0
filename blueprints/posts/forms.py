"""Форма публикации постов"""


# -- импорт модулей
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo


# -- форма регистрации
class PostForm(FlaskForm):
    subject = StringField(
        'Subject',
        validators=[
            DataRequired(),
            Length(min=5, max=32, message='От 5 до 32 символов')
        ]
    )
    
    content = TextAreaField(
        'Content',
        validators=[
            DataRequired(),
            Length(min=5, max=5000, message='От 5 до 5000 символов.')
        ]
    )

    submit = SubmitField('Опубликовать')