"""Файл шаблонов для главной страницы."""


# -- импорт модулей
from flask import url_for, redirect
from flask import Blueprint

bp = Blueprint('main', __name__)


@bp.route('/', methods=['GET'])
def index():
    return redirect(url_for('auth.login'))