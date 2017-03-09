#!/usr/bin/env python3
# coding=utf-8
"""Restaurador de base de datos basada en Flask"""
from flask import Flask, url_for, flash, redirect
from flask_login import LoginManager
from config import config
from .home import home
from .admin import admin
from .auth import auth
from .modelos.users import Users
from .restaurar import restaurar

login_manager = LoginManager()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    # Login manager
    login_manager.init_app(app)
    # Configuracion de los BluePrints
    app.register_blueprint(home)
    app.register_blueprint(auth)
    app.register_blueprint(restaurar, url_prefix='/restaurar')
    app.register_blueprint(admin, url_prefix='/admin')
    login_manager.login_view = 'auth.login'
    login_manager.use_session_for_next = True
    login_manager.login_message = 'Necesitas loguearte para acceder'
    return app


@login_manager.user_loader
def load_user(user_id):
    """
    This will be used many times like on using current_user
    :param user_id: username
    :return: user or none
    """
    return Users().get_user(user_id=user_id)
