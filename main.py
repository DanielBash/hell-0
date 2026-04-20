"""Файл запуска приложения"""

# - импорт модулей
from core.core import create_app
import settings
from core.flask_shortcuts import after_initialization
from core.logger import log


# - инициализация приложения
app = create_app(__name__)
log.info('Приложение создано')

if __name__ == '__main__':
    with app.app_context():
        after_initialization.main()
    app.run(settings.HOST, port=settings.PORT, debug=True)