"""Функция, запускающаяся после инициализации"""

import datetime

import settings
from apscheduler.schedulers.background import BackgroundScheduler
from flask import current_app
from .. import models
from core.core import create_admin_user, send_emails, posts_handler
from core.logger import log
from flask_migrate import upgrade, stamp
from filelock import FileLock
from ..models import ScheduledJob, db


lock = FileLock("migrations.lock")
scheduler = None


def _record_run(name, interval_minutes):
    job = ScheduledJob.query.filter_by(name=name).first()
    if job is None:
        job = ScheduledJob(name=name, interval_minutes=interval_minutes)
        db.session.add(job)
    job.last_run = datetime.datetime.utcnow()
    job.interval_minutes = interval_minutes
    db.session.commit()


def _run_posts(app):
    with app.app_context():
        try:
            posts_handler()
        except Exception as e:
            log.error(f'Ошибка обновления постов: {e}')
        _record_run('Обновление постов', 5)


def _run_emails(app):
    with app.app_context():
        try:
            send_emails()
        except Exception as e:
            log.error(f'Ошибка рассылки: {e}')
        _record_run('Рассылка имейлов', 60)


def main():
    global scheduler

    with lock:
        log.info("Миграции...")
        upgrade()

        log.info("Создание админ-пользователя...")
        create_admin_user()

    app = current_app._get_current_object()

    log.info("Запуск планировщика (посты — 5 мин, имейлы — 1 час)...")
    scheduler = BackgroundScheduler(daemon=True)
    now = datetime.datetime.now()
    scheduler.add_job(_run_posts, args=[app], trigger="interval", minutes=5, next_run_time=now)
    scheduler.add_job(_run_emails, args=[app], trigger="interval", hours=1, next_run_time=now)
    scheduler.start()


if __name__ == '__main__':
    main()
