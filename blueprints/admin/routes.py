"""Файл Админ-Панели."""


# -- импорт модулей
from flask import render_template, flash
from flask import Blueprint

from blueprints.admin.forms import SystemMessageForm
from core.core import post_add
from core.flask_shortcuts.decorators import required_permissions

bp = Blueprint('admin', __name__)


@bp.route('/', methods=['GET', 'POST'])
@required_permissions('VIEW_ADMIN_PANEL')
def index():
    form = SystemMessageForm()
    if form.validate_on_submit():
        post_add(form.category.data, form.text.data)
        flash('Сообщение успешно отправлено!', category='Сообщение')
        return render_template('admin.html', title='Админ-Панель', form=form)

    return render_template('admin.html', title='Админ-Панель', form=form)