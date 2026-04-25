import settings
from apscheduler.schedulers.background import BackgroundScheduler
from flask import current_app
from .. import models
from core.core import create_admin_user
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

        log.info("Планировка обновления новостей и рассылок...")
        app = current_app._get_current_object()

        def hourly_job():
            posts_handler()
            from core.mailer import send_newsletters
            send_newsletters(app)

        scheduler = BackgroundScheduler()
        scheduler.add_job(func=hourly_job, trigger="interval", hours=1)
        scheduler.start()


if __name__ == '__main__':
    main()
