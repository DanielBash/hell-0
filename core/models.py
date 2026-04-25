"""Инициализация базы данных"""

# -- импорт модулей
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy_serializer import SerializerMixin

import settings

db = SQLAlchemy()
socketio = None


# -- таблица пользователей
class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    # - скрытая информация
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(256), nullable=False)

    # - публичная информация
    permission_group = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(256), nullable=False)
    username = db.Column(db.String(32), nullable=False, unique=True, index=True)
    bio = db.Column(db.String(5000), nullable=False, default='')
    status = db.Column(db.String(30), nullable=False, default='')
    last_visit = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )
    registered_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )
    last_read = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    def get_permission(self, name):
        permissions = settings.PERMISSION_GROUPS.get(self.permission_group)
        if permissions is None:
            return None
        if name not in permissions:
            return None
        else:
            return permissions[name]


# -- таблица новостей-постов
class Post(db.Model, SerializerMixin):
    __tablename__ = "posts"

    # скрытая информация
    id = db.Column(db.Integer, primary_key=True)

    # публичная информация
    category = db.Column(db.String(50), nullable=False)
    data = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    def reaction_count(self, reaction_type=None):
        q = self.reactions
        if reaction_type:
            q = q.filter_by(reaction_type=reaction_type)
        return q.count()

    def user_reaction(self, user_id):
        return self.reactions.filter_by(user_id=user_id).first()


# -- таблица комментариев к постам
class PostComment(db.Model, SerializerMixin):
    __tablename__ = "post_comments"

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    post = db.relationship("Post", backref=db.backref("comments", lazy="dynamic"))
    body = db.Column(db.Text, nullable=False)
    title = db.Column(db.String(100), nullable=False, default='')
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", backref="comments")

    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def reaction_count(self, reaction_type=None):
        q = self.reactions
        if reaction_type:
            q = q.filter_by(reaction_type=reaction_type)
        return q.count()


# -- таблица реакций
class PostReaction(db.Model, SerializerMixin):
    __tablename__ = "post_reactions"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)

    reaction_type = db.Column(db.String(20), nullable=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())

    user = db.relationship("User", backref="reactions")
    post = db.relationship("Post", backref=db.backref("reactions", lazy="dynamic"))

    __table_args__ = (
        db.UniqueConstraint("user_id", "post_id", name="uq_user_post_reaction"),
    )


# -- таблица реакций на комментарии
class PostCommentReaction(db.Model, SerializerMixin):
    __tablename__ = "post_comment_reactions"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey("post_comments.id"), nullable=False)

    reaction_type = db.Column(db.String(20), nullable=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())

    user = db.relationship("User", backref="comment_reactions")
    post = db.relationship("PostComment", backref=db.backref("reactions", lazy="dynamic"))

    __table_args__ = (
        db.UniqueConstraint("user_id", "comment_id", name="uq_user_comment_reaction"),
    )


class MailSubscription(db.Model, SerializerMixin):
    __tablename__ = 'mail_subscriptions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    user = db.relationship('User', backref=db.backref('mail_subscription', uselist=False))
    send_days = db.Column(db.String(20), nullable=False, default='0,1,2,3,4,5,6')
    send_hour = db.Column(db.Integer, nullable=False, default=8)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    blocks = db.relationship('MailBlock', backref='subscription', cascade='all, delete-orphan')


class MailBlock(db.Model, SerializerMixin):
    __tablename__ = 'mail_blocks'

    id = db.Column(db.Integer, primary_key=True)
    subscription_id = db.Column(db.Integer, db.ForeignKey('mail_subscriptions.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    post_count = db.Column(db.Integer, nullable=False, default=2)