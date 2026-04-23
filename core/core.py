"""Ядро сайта. Логика прописана здесь"""

# -- импортирование модулей
from werkzeug.security import generate_password_hash, check_password_hash
import settings
from core.logger import log
from .models import PostReaction, Post, PostComment, db


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
        return False
    if check_password_hash(user.password, password):
        return True

    return False

from sqlalchemy.exc import IntegrityError

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