"""Файл шаблонов для показа рассылок."""


# -- импорт модулей
from flask import render_template
from flask import Blueprint
from core.flask_shortcuts.decorators import login_required


bp = Blueprint('mail', __name__)


@bp.route('/', methods=['GET'])
@login_required
def index():
    return render_template('mail_all.html', title='Рассылки')