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
    categories = [(settings.POST_CATEGORIES[i[0]]['readable'], i[0]) for i in
                  db.session.query(Post.category).distinct().all()]

    posts_by_category = dict()

    all_posts = Post.query.order_by(Post.created_at.desc()).all()

    for post in all_posts:
        category_name = post.category

        if category_name in posts_by_category:
            posts_by_category[category_name].append(post)
        else:
            posts_by_category[category_name] = [post]

    return render_template('news_all.html',
                           title='Новости',
                           posts_by_category=posts_by_category)


@bp.route('/category/<string:category>', methods=['GET'])
def category(category):
    readable_category = settings.POST_CATEGORIES[category]['readable']
    posts = Post.query.filter_by(category=category).all()
    return render_template('news_category.html', title=readable_category, posts=posts)
