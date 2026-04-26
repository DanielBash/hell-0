"""Ядро сайта. Логика прописана здесь"""
import datetime
import json
import smtplib
from email.mime.text import MIMEText

# -- импортирование модулей
from werkzeug.security import generate_password_hash, check_password_hash
import settings
from core.logger import log
from .models import PostReaction, Post, PostComment, db, PostCommentReaction, User
from sqlalchemy.exc import IntegrityError
from . import post_handlers


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
    for i in settings.POST_CATEGORIES:
        settings.POST_CATEGORIES[i]['handler']()


def send_email(user, force=False):
    import json
    import smtplib
    from datetime import datetime
    from email.mime.text import MIMEText
    from flask import render_template

    try:
        pref = json.loads(user.email_preference or "{}")
    except Exception:
        pref = {}

    if not pref and not force:
        return

    if not force:
        schedule = pref.get('schedule', {})
        hours = schedule.get('hours_utc', [])
        days = schedule.get('days', [])

        now = datetime.utcnow()
        if not (now.hour in hours and now.isoweekday() in days):
            return

    posts = []
    blocks = pref.get('blocks', [])

    for block in blocks:
        category = block.get('category_api_name')
        limit = block.get('max_number_of_posts', 3)

        if not category:
            continue

        query = (
            Post.query
            .filter_by(category=category)
            .filter(Post.created_at > user.last_read)
            .order_by(Post.created_at.desc())
            .limit(limit)
        )

        posts.extend(query.all())

    if not posts and not force:
        return

    html_body = render_template('email.html', posts=posts)

    if not html_body:
        return

    try:
        print(f'Отправка письма {user.email}')

        msg = MIMEText(html_body, "html", "utf-8")
        msg["Subject"] = "Новая рассылка"
        msg["From"] = settings.NEWSLETTER_EMAIL_INBOX
        msg["To"] = user.email

        with smtplib.SMTP(settings.NEWSLETTER_EMAIL_SERVER, 25) as server:
            server.starttls()
            server.login(
                settings.NEWSLETTER_EMAIL_INBOX,
                settings.NEWSLETTER_EMAIL_PASSWORD
            )
            server.send_message(msg)

        user.last_read = datetime.utcnow()
        db.session.commit()

    except Exception as e:
        print(f"Ошибка отправки письма {e}")


def send_emails(force=False):
    for i in User.query.all():
        send_email(user=i, force=force)
