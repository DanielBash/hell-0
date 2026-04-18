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
