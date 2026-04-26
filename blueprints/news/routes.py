"""Файл шаблонов для показа новостей."""

from flask import render_template, request, jsonify, redirect, url_for
from flask import Blueprint
import datetime
from blueprints.news.forms import CommentForm
from core.flask_shortcuts.decorators import login_required
from core.models import db, Post, PostReaction, PostComment, PostCommentReaction, UserCategoryRead
import settings
from core.core import set_reaction, set_reaction_comment, post_comment_add
from flask import g


bp = Blueprint('news', __name__)


@bp.route('/', methods=['GET'])
def index():
    categories = [[settings.POST_CATEGORIES[i[0]]['readable'], i[0], 0] for i in db.session.query(Post.category).distinct().all()]

    if g.user:
        reads = {r.category: r.last_read for r in UserCategoryRead.query.filter_by(user_id=g.user.id).all()}

        for i in range(len(categories)):
            cat = categories[i][1]
            last_read = reads.get(cat)
            if last_read:
                count = Post.query.filter_by(category=cat).filter(Post.created_at > last_read).count()
            else:
                count = Post.query.filter_by(category=cat).count()
            categories[i][2] = count

    return render_template('news_all.html', title='Новости', categories=categories)


@bp.route('/category/<string:category>', methods=['GET'])
def category(category):
    readable_category = settings.POST_CATEGORIES[category]['readable']
    posts = Post.query.filter_by(category=category).order_by(Post.created_at).all()

    if g.user:
        now = datetime.datetime.utcnow()
        read = UserCategoryRead.query.filter_by(user_id=g.user.id, category=category).first()
        if read:
            read.last_read = now
        else:
            db.session.add(UserCategoryRead(user_id=g.user.id, category=category, last_read=now))
        db.session.commit()

    return render_template('news_category.html', title=readable_category, posts=posts, reactions=settings.POST_REACTIONS)


@bp.route('/react/<int:post_id>', methods=['POST'])
@login_required
def react(post_id):
    reaction_type = request.form.get('reaction')
    set_reaction(g.user.id, post_id, reaction_type)

    post = Post.query.get_or_404(post_id)
    counts = {key: post.reaction_count(key) for key in settings.POST_REACTIONS}
    user_reaction = post.user_reaction(g.user.id)
    return jsonify({
        'counts': counts,
        'user_reaction': user_reaction.reaction_type if user_reaction else None,
    })


@bp.route('/react_comment/<int:comment_id>', methods=['POST'])
@login_required
def react_comment(comment_id):
    reaction_type = request.form.get('reaction')
    set_reaction_comment(g.user.id, comment_id, reaction_type)

    comment = PostComment.query.get_or_404(comment_id)
    counts = {key: comment.reaction_count(key) for key in settings.POST_REACTIONS}
    user_reaction = PostCommentReaction.query.filter_by(user_id=g.user.id, comment_id=comment_id).first()
    return jsonify({
        'counts': counts,
        'user_reaction': user_reaction.reaction_type if user_reaction else None,
    })


@bp.route('/<int:post_id>/comments', methods=['GET', 'POST'])
@login_required
def comments(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()

    if form.validate_on_submit():
        post_comment_add(form.text.data, g.user.id, post_id)
        return redirect(url_for('news.comments', post_id=post_id))

    comments = PostComment.query.filter_by(post_id=post_id).all()
    return render_template('news_comments.html', title='Комментарии к посту', post=post, comments=comments,
                           reactions=settings.POST_REACTIONS, form=form)
