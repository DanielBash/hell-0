"""Файл API."""


# -- импорт модулей
from flask import render_template
from flask import Blueprint

bp = Blueprint('api', __name__)


@bp.route('/', methods=['GET'])
def index():
    return render_template('api.html', title='Апи')