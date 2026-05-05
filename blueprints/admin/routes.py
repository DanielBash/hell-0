"""Файл Админ-Панели."""


# -- импорт модулей
from flask import render_template, flash, redirect, url_for
from flask import Blueprint

from blueprints.admin.forms import SystemMessageForm
from core.core import post_add, posts_handler, send_emails
from core.flask_shortcuts.decorators import required_permissions
from core.logger import log
from core.models import ScheduledJob

bp = Blueprint('admin', __name__)


def _render(form):
    jobs = ScheduledJob.query.order_by(ScheduledJob.name).all()
    return render_template('admin.html', title='Админ-Панель', form=form, jobs=jobs)


@bp.route('/', methods=['GET', 'POST'])
@required_permissions('VIEW_ADMIN_PANEL')
def index():
    form = SystemMessageForm()
    if form.validate_on_submit():
        post_add(form.category.data, form.text.data)
        flash('Сообщение успешно отправлено!', category='Сообщение')
        return _render(form)

    return _render(form)


@bp.route('/posts_update', methods=['GET', 'POST'])
@required_permissions('VIEW_ADMIN_PANEL')
def posts_update():
    print('Обновляем посты')
    posts_handler()
    flash('Посты успешно обновлены!')
    return redirect(url_for('admin.index'))


@bp.route('/emails_send', methods=['GET', 'POST'])
@required_permissions('VIEW_ADMIN_PANEL')
def send_emails_force():
    print('Отправляем имейлы')
    send_emails(force=True)
    flash('Имейлы успешно отправлены!')
    return redirect(url_for('admin.index'))