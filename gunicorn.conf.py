# -*- coding: utf-8 -*-
"""
Gunicorn with Uvicorn config to launch in Digital Ocean's App Platform.
"""
bind = "0.0.0.0:8080"
workers = 4
# Uvicorn's Gunicorn worker class
worker_class = "uvicorn.workers.UvicornWorker"
