FROM python:3.12-slim

WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt
RUN mkdir -p /var/log/gunicorn && chmod 755 /var/log/gunicorn

CMD ["gunicorn", "--config", "gunicorn_config.py", "main:app"]