"""Функция, запускающаяся после инициализации"""


# -- importing modules
import settings
from flask import current_app
from .. import models
from core.core import create_admin_user
from core.logger import log


def main():
    log.info('Создвние админ-пользователя.')
    create_admin_user()


if __name__ == '__main__':
    main()
