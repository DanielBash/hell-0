"""Настройки по-умолчанию"""

# -- импорт модулей
from pathlib import Path
from secrets import token_hex

# -- настройки Flask
PORT = 8080  # порт
HOST = '0.0.0.0'  # хост
SECRET_KEY = token_hex(128)  # секретный криптографический ключ; для production задайте SECRET_KEY в .env

# -- настройки приложения
DEBUG = False  # режим отладки
PRINT_CONSTANTS = True  # вывод настроек перед инициализацией

# -- настройки базы данных
SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'  # путь к базе данных
TEMPLATE_PATH = Path('templates')  # файл шаблонов
SKIP_DB_INIT = False

# -- настройки шаблонов
BASE_BLUEPRINTS = ['main', 'index']  # шаблоны которые будут обрабатываться без префикса

# -- настройки привелегий
PERMISSION_GROUPS = {
    'admin': {
        'VIEW_ADMIN_PANEL': True,
    },
    'user': {
        'VIEW_ADMIN_PANEL': False,
    }
}

# -- данные пользователя админ
ADMIN_PASSWORD = 'password'
ADMIN_USERNAME = 'admin'
ADMIN_PERMISSION_GROUP = 'admin'
ADMIN_EMAIL = 'inbox@example.com'
ADMIN_BIO = 'Я администратор и главный разработчик сайта.'
ADMIN_STATUS = 'Модерирую новости. Слежу за жалобами.'

# -- настройки пользователей по-умолчанию
DEFAULT_PERMISSION_GROUP = 'user'
DEFAULT_STATUS = 'Исследователь'
DEFAULT_BIO = f'Я активно слежу за последними новостями'

POST_REACTIONS = {
    "like": "👍",
    "love": "❤️",
    "laugh": "😂",
    "wow": "😮"
}

POST_CATEGORIES = {}

NEWSLETTER_EMAIL_PASSWORD='password'
NEWSLETTER_EMAIL_SERVER='smtp.example.com'
NEWSLETTER_EMAIL_INBOX='inbox@example.com'