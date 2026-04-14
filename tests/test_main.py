"""Тестирование основных функций приложения"""


# - проверить доступность ресурса
def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200