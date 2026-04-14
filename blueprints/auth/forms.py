"""Формы авторизации"""


# -- импортирование модулей
from flask_wtf import FlaskForm
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
        'Email',
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
    bio = TextAreaField(label='Обо мне', validators=[DataRequired(), Length(max=5000, message='Bio must be shorter then 5k symbols.')])
    status = StringField(label='Статус', validators=[DataRequired(), Length(min=5, max=30, message='Status must be at least 5 charecters and no more then 30.')])
    submit = SubmitField('Применить')