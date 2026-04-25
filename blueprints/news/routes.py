"""Файл шаблонов для показа новостей."""
from pyexpat.errors import messages

# -- импорт модулей
from flask import render_template
from flask import Blueprint
from core.models import db, Post
import settings

bp = Blueprint('news', __name__)


@bp.route('/', methods=['GET'])
def index():
    categories = [(settings.POST_CATEGORIES[i[0]]['readable'], i[0]) for i in db.session.query(Post.category).distinct().all()]

    return render_template('news_all.html', title='Новости', categories=categories)

@bp.route('/category/<string:category>', methods=['GET'])
def category(category):
    readable_category = settings.POST_CATEGORIES[category]['readable']
    posts = Post.query.filter_by(category=category).all()
    return render_template('news_category.html', title=readable_category, posts=posts)