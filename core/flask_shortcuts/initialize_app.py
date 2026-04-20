""" - Инициализация фласк-приложения"""

from flask import Flask, g
from ..models import db
import settings
from . import jinja_filters
from . import after_initialization
from ..logger import log
from flask_migrate import Migrate


# - инициализация приложения
def create_app(name) -> Flask:
    app = Flask(name)
    migrate = Migrate()
    app.config.from_object(settings.FLASK_SETTINGS)

    db.init_app(app)
    migrate.init_app(app, db)

    log.info('Инициализация шаблонов')
    with app.app_context():
        from blueprints import blueprints

        for bp in blueprints:
            if bp not in settings.BASE_BLUEPRINTS:
                app.register_blueprint(blueprints[bp], url_prefix=f'/{bp}')
            else:
                app.register_blueprint(blueprints[bp])

    for key, val in jinja_filters.jinja_filters.items():
        app.jinja_env.filters[key] = val

    with app.app_context():
        from . import context_processors
        from . import before_request

    return app
