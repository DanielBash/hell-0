"""Файл шаблонов для показа новостей."""


# -- импорт модулей
from flask import render_template
from flask import Blueprint

bp = Blueprint('news', __name__)


@bp.route('/', methods=['GET'])
def index():
    return render_template('news_all.html')