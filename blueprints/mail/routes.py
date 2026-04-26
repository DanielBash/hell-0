"""Файл шаблонов для показа рассылок."""
import flask
# -- импорт модулей
from flask import render_template, request
from flask import Blueprint
from werkzeug.utils import redirect
from flask import g
import json
from core.flask_shortcuts.decorators import login_required
from core.models import db
from settings import POST_CATEGORIES

bp = Blueprint('mail', __name__)


@bp.route('/', methods=['GET'])
@login_required
def index():
    categories = {}
    for i in POST_CATEGORIES:
        categories[i] = {}
        categories[i]['readable'] = POST_CATEGORIES[i]['readable']
    return render_template('mail_all.html', title='Рассылки',
                           categories=categories) # {'category_api_name': {'readable': 'readable category name'}}

@bp.route('set/', methods=['POST'])
@login_required
def set_preference():
    try:
        data = request.json
        g.user.email_preference = json.dumps(data)
        db.session.commit()
        return 'done'
    except:
        return 'failed'


@bp.route('get/', methods=['POST', 'GET'])
@login_required
def get_preference():
    try:
        return flask.jsonify(json.loads(g.user.email_preference))
    except:
        return flask.jsonify({})