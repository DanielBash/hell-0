"""Общий контекст тестов"""

# -- импорт модулей
import os
import pytest
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import main


# - приложение
@pytest.fixture()
def app():
    app = main.app
    app.config.update({"TESTING": True, "WTF_CSRF_ENABLED": False})
    yield app


# - клиент приложения
@pytest.fixture()
def client(app):
    return app.test_client()
