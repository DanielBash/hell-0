"""Инициализация базы данных"""

# -- импорт модулей
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.mutable import MutableDict
import settings

db = SQLAlchemy()
socketio = None


# -- таблица пользователей
class User(db.Model):
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

    def get_permission(self, name):
        permissions = settings.PERMISSION_GROUPS[self.permission_group]

        if name not in permissions:
            return None
        else:
            return permissions[name]


# -- таблица новостей-постов
class Post(db.Model):
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


# -- таблица комментариев к постам
class PostComment(db.Model):
    __tablename__ = "post_comments"

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    post = db.relationship("Post", backref=db.backref("comments", lazy="dynamic"))
    body = db.Column(db.Text, nullable=False)
    title = db.Column(db.String(100), nullable=False, default='')
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", backref="comments")

    created_at = db.Column(db.DateTime, server_default=db.func.now())


# -- таблица реакция
class PostReaction(db.Model):
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

    def reaction_count(self, reaction_type=None):
        q = self.reactions
        if reaction_type:
            q = q.filter_by(reaction_type=reaction_type)
        return q.count()

    def user_reaction(self, user_id):
        return self.reactions.filter_by(user_id=user_id).first()