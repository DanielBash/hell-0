"""Функция, запускающаяся после инициализации"""

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

        app = current_app._get_current_object()

        def _posts_handler_job():
            with app.app_context():
                posts_handler()

        def _send_emails_job():
            with app.app_context():
                send_emails()

        log.info("Планировка обновления новостей (каждые 5 минут)...")
        scheduler = BackgroundScheduler()
        scheduler.add_job(func=_posts_handler_job, trigger="interval", minutes=5)
        scheduler.add_job(func=_send_emails_job, trigger="interval", minutes=5)
        scheduler.start()


if __name__ == '__main__':
    main()
