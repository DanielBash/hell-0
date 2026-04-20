"""Настройки gunicorn."""

bind = "0.0.0.0:8080"
workers = 1
worker_class = "eventlet"
worker_connections = 1000
timeout = 30
keepalive = 2
spew = False

accesslog = "-"
errorlog = "-"

loglevel = "info"

proc_name = "hell_0_gunicorn"
