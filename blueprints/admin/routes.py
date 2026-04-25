from flask import render_template, flash, redirect, url_for
from flask import Blueprint

from blueprints.admin.forms import SystemMessageForm, ActionForm
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
        return render_template('admin.html', title='Админ-Панель',
                               form=form, handlers_form=ActionForm(), mail_form=ActionForm())

    return render_template('admin.html', title='Админ-Панель',
                           form=form, handlers_form=ActionForm(), mail_form=ActionForm())


@bp.route('/update-handlers', methods=['POST'])
@required_permissions('VIEW_ADMIN_PANEL')
def update_handlers():
    from core.handlers import run_all
    run_all()
    flash('Новости обновлены!', 'Сообщение')
    return redirect(url_for('admin.index'))


@bp.route('/send-emails', methods=['POST'])
@required_permissions('VIEW_ADMIN_PANEL')
def send_emails():
    from flask import current_app
    from core.mailer import send_newsletters
    send_newsletters(current_app._get_current_object())
    flash('Рассылки отправлены!', 'Сообщение')
    return redirect(url_for('admin.index'))
