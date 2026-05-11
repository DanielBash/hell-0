"""Тестирование основных функций приложения"""


# - проверить доступность ресурса
def test_home_page(client):
    response = client.get('/docs')
    assert response.status_code == 302
