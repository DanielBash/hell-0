"""Настройки по-умолчанию"""

# -- импорт модулей
from pathlib import Path
from secrets import token_hex

# -- настройки Flask
PORT = 8080  # порт
HOST = '0.0.0.0'  # хост
SECRET_KEY = token_hex(128)  # секретный криптографический ключ

# -- настройки приложения
DEBUG = False  # режим отладки
PRINT_CONSTANTS = True  # вывод настроек перед инициализацией

# -- настройки базы данных
SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'  # путь к базе данных
TEMPLATE_PATH = Path('templates')  # файл шаблонов

# -- настройки шаблонов
BASE_BLUEPRINTS = ['main', 'index']  # шаблоны которые будут обрабатываться без префикса

# -- настройки привелегий
PERMISSION_GROUPS = {
    'admin': {
        'VIEW_ADMIN_PANEL': True,
        'SEND_MAIL_MESSAGES': True,
        'PUBLUSH_POSTS': True,
    },
    'user': {
        'VIEW_ADMIN_PANEL': False,
        'SEND_MAIL_MESSAGES': True,
        'PUBLUSH_POSTS': True,
    }
}

# -- данные пользователя админ
ADMIN_PASSWORD = 'password'
ADMIN_USERNAME = 'admin'
ADMIN_PERMISSION_GROUP = 'admin'
ADMIN_EMAIL = 'hidden@example.com'
ADMIN_BIO = 'Я админ этого сайта.'
ADMIN_STATUS = 'Создаю нечто великолепное...'

# -- настройки пользователей по-умолчанию
DEFAULT_PERMISSION_GROUP = 'user'
DEFAULT_STATUS = 'Гик'
DEFAULT_BIO = f'Я гик и буду гиковать.'

# -- front end estetics
# - pagination
MESSAGES_PAGINATION = 20
POSTS_PAGINATION = 10
