#!/usr/bin/env python3
# coding=utf-8
"""Restaurador de base de datos basada en Flask"""
from flask import Flask
from config import config
from .home import home
from .admin import admin
from .auth import auth
from .restaurar import restaurar


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    # Configuracion de los BluePrints
    app.register_blueprint(home)
    app.register_blueprint(auth)
    app.register_blueprint(restaurar, url_prefix='/restaurar')
    app.register_blueprint(admin, url_prefix='/admin')
    return app
