from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, SelectField, BooleanField, SubmitField
from wtforms.widgets import ListWidget, CheckboxInput

DAYS = [(str(i), d) for i, d in enumerate(['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'])]
HOURS = [(str(i), f'{i:02d}:00') for i in range(24)]


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class SubscriptionForm(FlaskForm):
    send_days = MultiCheckboxField('Дни отправки', choices=DAYS)
    send_hour = SelectField('Час отправки', choices=HOURS, coerce=int)
    is_active = BooleanField('Активна')
    submit = SubmitField('Сохранить')
