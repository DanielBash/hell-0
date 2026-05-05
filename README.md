![placeholder](https://github.com/DanielBash/hell-0/blob/main/.github/github-banner.png?raw=true)
![Python](https://img.shields.io/badge/python-3.12%2B-blue)
![Stars](https://img.shields.io/github/stars/DanielBash/hell-0)
[![.github/workflows/python-tests.yaml](https://github.com/DanielBash/hell-0/actions/workflows/python-tests.yaml/badge.svg)](https://github.com/DanielBash/hell-0/actions/workflows/python-tests.yaml)
[![update-docker-image](https://github.com/DanielBash/hell-0/actions/workflows/docker-deploy.yaml/badge.svg)](https://github.com/DanielBash/hell-0/actions/workflows/docker-deploy.yaml)

# hell-0

> Положите руку на пульс человечества.

Новости из разных ресурсов в одном месте. Делитесь, обсуждайте, подписывайтесь на новости из разных источников, со всех концов интернета. Веб-Сайт доступен по [ссылке](https://hell-0.ru)!

## Локальный запуск
### Способ 1: Виртуальное окружение
1) Скачайте репозиторий
```bash
git clone https://github.com/DanielBash/profile.git
cd profile
```

2) Установите необходимые зависимости
```bash
pip install -r requirements.txt
```

3) По необходимости поменяйте настройки в файле .env <br/>
```bash
touch .env
echo "SECRET_KEY=secure-secret-key" > .env
```

4) Запустите сервер <br/>

**Способ 1.1**: Запуск в режиме отладки
```bash
python main.py
```

**Способ 1.2**: Запуск на продакшене
```bash
gunicorn --config gunicorn_config.py main:app
```

### Способ 2: Докер-контейнер
1) Загрузите последнюю версию докер-изображения:
```bash
docker pull danielbashl/hell-0:latest
```

2) Запустите контейнер:
```bash
docker run -d -p 8000:5000 danielbashl/hell-0:latest
```

