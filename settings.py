"""Инициализация настроек всего проекта."""


# - импорт модулей
import dotenv
import importlib
import os
from core.logger import log


# -- загрузка шаблона настроек
dotenv.load_dotenv()
settings_template = os.environ.get('SETTINGS_TEMPLATE', 'settings_templates.default')
if not settings_template.startswith('settings_templates.'):
    settings_template = 'settings_templates.' + settings_template

module = importlib.import_module(settings_template)

for key in dir(module):
    if key.isupper():
        globals()[key] = getattr(module, key)

# -- загрузка переменный окружения из файла .env
globals().update({
    k: v for k, v in os.environ.items()
    if k.isupper()
})


# -- создание объекта настроек Flask
class FlaskSettings:
    def __init__(self):
        for key, value in globals().items():
            if key.isupper():
                setattr(self, key, value)


FLASK_SETTINGS = FlaskSettings()

# -- вывод настроек, после инициализации приложения
if PRINT_CONSTANTS and os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    log.info('Настройки загружены, вот они:')
    for i in dir(module):
        if i.isupper():
            log.rich(f'[red]{i}[/] = {globals()[i]}')