# coding=utf-8
from functools import wraps
from flask_login import current_user
from flask import current_app, redirect, url_for, flash

def is_admin(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.admin:
            flash('Necesita ser administrador para acceder', 'error')
            return redirect(url_for('home.index'))
        return func(*args, **kwargs)
    return decorated_view

def is_not_consulta(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.consulta:
            flash('Su rol no le permite acceder a este módulo', 'error')
            return redirect(url_for('home.index'))
        return func(*args, **kwargs)
    return decorated_view
