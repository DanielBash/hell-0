"""Инициализация базы данных"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy_serializer import SerializerMixin

import settings

db = SQLAlchemy()
socketio = None


class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(256), nullable=False)

    permission_group = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(256), nullable=False)
    username = db.Column(db.String(32), nullable=False, unique=True, index=True)
    bio = db.Column(db.String(5000), nullable=False, default='')
    status = db.Column(db.String(30), nullable=False, default='')
    last_visit = db.Column(db.DateTime, server_default=db.func.now())
    registered_at = db.Column(db.DateTime, server_default=db.func.now())
    last_read = db.Column(db.DateTime, server_default=db.func.now())
    last_email_sent = db.Column(db.DateTime, server_default=db.func.now())
    email_preference = db.Column(db.Text, default='{}')

    def get_permission(self, name):
        permissions = settings.PERMISSION_GROUPS.get(self.permission_group)
        if permissions is None:
            return None
        if name not in permissions:
            return None
        else:
            return permissions[name]


class UserCategoryRead(db.Model, SerializerMixin):
    __tablename__ = "user_category_reads"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    last_read = db.Column(db.DateTime, server_default=db.func.now())

    user = db.relationship("User", backref="category_reads")

    __table_args__ = (
        db.UniqueConstraint("user_id", "category", name="uq_user_category_read"),
    )


class Post(db.Model, SerializerMixin):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
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