"""Функция, запускающаяся после инициализации"""

# -- импорт модулей
import settings
from apscheduler.schedulers.background import BackgroundScheduler
from flask import current_app
from .. import models
from core.core import create_admin_user, send_emails
from core.logger import log
from flask_migrate import upgrade, stamp
from filelock import FileLock
from ..core import posts_handler


lock = FileLock("migrations.lock")

def main():

    with lock:
        log.info("Миграции...")
        upgrade()

        log.info("Создание админ-пользователя...")
        create_admin_user()

        log.info("Планировка обновления новостей...")
        scheduler = BackgroundScheduler()
        scheduler.add_job(func=posts_handler, trigger="interval", hours=0.1)
        scheduler.add_job(func=send_emails, trigger="interval", hours=0.1)
        scheduler.start()


if __name__ == '__main__':
    main()
