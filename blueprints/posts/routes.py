"""Шаблоны постов"""


# -- импорт модулей
import datetime
from flask import current_app, flash, g, redirect, url_for, request
from flask import Blueprint, render_template
from settings_templates.default import POSTS_PAGINATION
from .forms import PostForm
from core.models import db, Post, User
import settings

bp = Blueprint('posts', __name__)


@bp.route('/<string:username>', methods=['GET', 'POST'])
def posts(username):
    form = PostForm()
    
    if form.validate_on_submit():
        if not g.user:
            return redirect(url_for('auth.login'))
        
        if not g.user.get_permission('PUBLUSH_POSTS'):
            flash('Вам запрещено публиковать посты', "Неудача")
            return redirect(url_for('posts.posts', username=username))
        
        post = Post(
            content=form.data['content'],
            subject=form.data['subject'],
            user_id=g.user.id
        )
        
        db.session.add(post)
        db.session.commit()
        
        flash('Ваш пост был опубликован!', 'Успех')
        
        return redirect(url_for('posts.posts', username=username))
    
    target_user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get("page", 1, type=int)

    pagination = Post.query\
        .filter_by(
            user_id=target_user.id
        )\
        .order_by(Post.published_at.desc())\
        .paginate(page=page, per_page=settings.POSTS_PAGINATION)

    posts = pagination.items
    
    if g.user is not None and target_user.id == g.user.id:
        return render_template(
            "posts.html",
            posts=posts,
            pagination=pagination,
            title='Посты',
            form=form,
            target_user=target_user
        )
    else:
        return render_template(
            "posts.html",
            posts=posts,
            pagination=pagination,
            title='Посты',
            form=False,
            target_user=target_user
        )


@bp.route('/view/<int:id>', methods=['GET'])
def post(id):
    post = Post.query.get_or_404(id)
    target_user = User.query.filter_by(id=post.user_id).first_or_404()
    
    return render_template(
        "post.html",
        post=post,
        target_user=target_user,
        title='Post',
    )