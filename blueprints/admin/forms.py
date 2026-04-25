from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.fields.choices import SelectField
import settings

system_choices = [(i, settings.POST_CATEGORIES[i]['readable']) for i in settings.POST_CATEGORIES.keys()]

class SystemMessageForm(FlaskForm):
    text = TextAreaField(label='Сообщение')
    category = SelectField(label='Категория', choices=system_choices)
    submit = SubmitField('Отправить')