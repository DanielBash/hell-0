"""Формы авторизации"""


# -- импортирование модулей
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo


# -- форма регистрации
class RegistrationForm(FlaskForm):
    username = StringField(
        'Имя пользователя',
        validators=[
            DataRequired(),
            Length(min=4, max=32, message='Имя пользователя от 4 до 32 символов.')
        ]
    )
    email = StringField(
        'Почтовый ящик',
        validators=[
            DataRequired(),
            Email(message='Введите свою почту в формате <ящик>@<сервер>.')
        ]
    )
    password = PasswordField(
        'Придумайте пароль',
        validators=[
            DataRequired(),
            Length(min=8, message='Пароль должен быть не меньше 8ми символов.')
        ]
    )
    confirm_password = PasswordField(
        'Повторите пароль',
        validators=[
            DataRequired(),
            EqualTo('password', message='Пароли должны совпадать.')
        ]
    )

    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    username = StringField(
        'Имя пользователя',
        validators=[
            DataRequired(),
        ]
    )
    password = PasswordField(
        'Пароль',
        validators=[DataRequired()]
    )
    submit = SubmitField('Войти')


class ProfileEditForm(FlaskForm):
    bio = TextAreaField(label='Обо мне', validators=[DataRequired(), Length(max=5000, message='Не длинее 5000 символов.')])
    status = StringField(label='Статус', validators=[DataRequired(), Length(min=5, max=30, message='Хотябы 5 и меньше 31')])
    picture = FileField(label='Аватар', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Только изображения.')])
    submit = SubmitField('Применить')