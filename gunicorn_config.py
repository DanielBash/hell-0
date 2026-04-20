"""Настройки gunicorn."""

bind = "0.0.0.0:8080"
workers = 1
worker_class = "gevent"
worker_connections = 1000
timeout = 30
keepalive = 5
spew = False

accesslog = "-"
errorlog = "-"

loglevel = "info"

proc_name = "hell_0_gunicorn"
