#!/usr/bin/env python3
# coding=utf-8
"""Restaurador de base de datos basada en Flask"""
from flask import Flask, url_for, flash
from flask import request, redirect, current_app, session
from flask_login import LoginManager
from config import config
from .home import home
from .admin import admin
from .api import api
from .auth import auth
from .consolidacion import consolidacion
from .monitorear import monitorear
from .historial import historial
from .restaurar import restaurar
from .versiones import versiones
from .modelos.users import Users

login_manager = LoginManager()

def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    # Login manager
    login_manager.init_app(app)
    # Configuracion de los BluePrints
    app.register_blueprint(home)
    app.register_blueprint(auth)
    app.register_blueprint(restaurar, url_prefix='/restaurar')
    app.register_blueprint(monitorear, url_prefix='/monitorear')
    app.register_blueprint(historial, url_prefix='/historial')
    app.register_blueprint(versiones, url_prefix='/versiones')
    app.register_blueprint(consolidacion, url_prefix='/consolidacion')
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(api, url_prefix='/api/v1')
    # Pagination helper
    app.jinja_env.globals['url_for_other_page'] = url_for_other_page
    login_manager.login_view = 'auth.login'
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
