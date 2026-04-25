from flask import render_template, flash, redirect, url_for
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


@bp.route('/update-handlers', methods=['POST'])
@required_permissions('VIEW_ADMIN_PANEL')
def update_handlers():
    from core.handlers import run_all
    run_all()
    flash('Новости обновлены!', 'Сообщение')
    return redirect(url_for('admin.index'))
