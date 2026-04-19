"""Файл шаблонов для описания проектов."""


# -- импорт модулей
from flask import render_template
from flask import Blueprint

bp = Blueprint('docs', __name__)


@bp.route('/', methods=['GET'])
def index():
    return render_template('docs.html')