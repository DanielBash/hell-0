from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.fields.choices import SelectField
from wtforms.validators import Length, DataRequired
import settings


class CommentForm(FlaskForm):
    text = TextAreaField(label='Комментарий', validators=[Length(min=4, max=32), DataRequired()])
    submit = SubmitField('Отправить')