"""Файл шаблонов для главной страницы."""


# -- импорт модулей
import datetime
from flask import current_app, flash
from flask import Blueprint, render_template

bp = Blueprint('main', __name__)


@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html', title='hell-0')