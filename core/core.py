"""Ядро сайта. Логика прописана здесь"""

# -- импортирование модулей
from werkzeug.security import generate_password_hash, check_password_hash
import settings
from core.logger import log
from .models import PostReaction, Post, PostComment, db, PostCommentReaction
from sqlalchemy.exc import IntegrityError


def create_app(name):
    from .flask_shortcuts import initialize_app
    return initialize_app.create_app(name)


def create_admin_user():
    register_user(settings.ADMIN_USERNAME, settings.ADMIN_PASSWORD, permission_group=settings.ADMIN_PERMISSION_GROUP,
                  email=settings.ADMIN_EMAIL, bio=settings.ADMIN_BIO, status=settings.ADMIN_STATUS)


def register_user(username, password, email,
                  permission_group=settings.DEFAULT_PERMISSION_GROUP, status=settings.DEFAULT_STATUS,
                  bio=settings.DEFAULT_BIO):
    from .models import User, db

    does_username_exist = User.query.filter_by(username=username).count()

    if does_username_exist > 0:
        return

    user = User(
        username=username,
        password=generate_password_hash(password),
        permission_group=permission_group,
        email=email,
        bio=bio,
        status=status
    )

    db.session.add(user)
    db.session.commit()

    log.info(f'Пользователь создан: {username}')

    return user


def check_credentials(username, password):
    from .models import User, db

    user = User.query.filter_by(username=username).first()
    if user is None:
        return None
    if check_password_hash(user.password, password):
        return user
    return None

def set_reaction(user_id, post_id, reaction_type):
    reaction = PostReaction(
        user_id=user_id,
        post_id=post_id,
        reaction_type=reaction_type,
    )
    try:
        db.session.add(reaction)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        existing = PostReaction.query.filter_by(
            user_id=user_id,
            post_id=post_id,
        ).first()
        if existing:
            existing.reaction_type = reaction_type
            db.session.commit()

def set_reaction_comment(user_id, post_id, reaction_type):
    reaction = PostCommentReaction(
        user_id=user_id,
        comment_id=post_id,
        reaction_type=reaction_type,
    )
    try:
        db.session.add(reaction)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        existing = PostCommentReaction.query.filter_by(
            user_id=user_id,
            comment_id=post_id,
        ).first()
        if existing:
            existing.reaction_type = reaction_type
            db.session.commit()

def post_add(category, data):
    new_post = Post(category=category, data=data)
    db.session.add(new_post)
    db.session.commit()

def post_comment_add(body, user_id, post_id):
    new_post = PostComment(post_id=post_id, user_id=user_id, body=body)
    db.session.add(new_post)
    db.session.commit()


def posts_handler():
    from core.handlers import run_all
    run_all()