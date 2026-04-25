"""Файл шаблонов для показа новостей."""


# -- импорт модулей
from flask import render_template, request, jsonify, redirect, url_for
from flask import Blueprint
from sqlalchemy import func
import datetime
from blueprints.news.forms import CommentForm
from core.flask_shortcuts.decorators import login_required
from core.models import db, Post, PostReaction, PostComment
import settings
from core.core import set_reaction, set_reaction_comment, post_comment_add
from flask import g


bp = Blueprint('news', __name__)


@bp.route('/', methods=['GET'])
def index():
    categories = [[settings.POST_CATEGORIES[i[0]]['readable'], i[0], 0] for i in db.session.query(Post.category).distinct().all()]

    if g.user:
        counts = dict(
            db.session.query(Post.category, func.count())
            .filter(Post.created_at >= g.user.last_read)
            .group_by(Post.category)
            .all()
        )

        for i in range(len(categories)):
            categories[i][2] = counts.get(categories[i][1], 0)

    return render_template('news_all.html', title='Новости', categories=categories)

@bp.route('/category/<string:category>', methods=['GET'])
def category(category):
    readable_category = settings.POST_CATEGORIES[category]['readable']
    posts = Post.query.filter_by(category=category).order_by(Post.created_at).all()
    if g.user:
        g.user.last_read = datetime.datetime.utcnow()
        db.session.commit()

    return render_template('news_category.html', title=readable_category, posts=posts, reactions=settings.POST_REACTIONS)

@bp.route('/react/<int:post_id>', methods=['POST'])
@login_required
def react(post_id):
    reaction_type = request.form.get('reaction')

    set_reaction(g.user.id, post_id, reaction_type)
    return redirect(request.referrer or url_for('main.index'))

@bp.route('/react_comment/<int:post_id>', methods=['POST'])
@login_required
def react_comment(post_id):
    reaction_type = request.form.get('reaction')

    set_reaction_comment(g.user.id, post_id, reaction_type)
    return redirect(request.referrer or url_for('main.index'))

@bp.route('/<int:post_id>/comments', methods=['GET', 'POST'])
@login_required
def comments(post_id):
    comments = PostComment.query.filter_by(post_id=post_id).all()
    post = Post.query.get_or_404(post_id)
    form = CommentForm()

    if form.validate_on_submit():
        post_comment_add(form.text.data, g.user.id, post_id)

    return render_template('news_comments.html', title='Комментарии к посту', post=post, comments=comments,
                           reactions=settings.POST_REACTIONS, form=form)
