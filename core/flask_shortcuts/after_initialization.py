"""Функция, запускающаяся после инициализации"""


# -- importing modules
import settings
from flask import current_app
from .. import models
from core.core import create_admin_user
from core.logger import log
from flask_migrate import upgrade, stamp
from filelock import FileLock


lock = FileLock("migrations.lock")

def main():

    with lock:
        log.info("Миграции...")
        upgrade()

        log.info("Создание админ-пользователя...")
        create_admin_user()


if __name__ == '__main__':
    main()
