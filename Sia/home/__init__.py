# coding=utf-8
from flask import Blueprint, render_template, request
from flask_login import login_required

home = Blueprint(
    'home',
    __name__,
    template_folder='templates'
)


@home.route('/')
@login_required
def index():
    """index"""
    return render_template('index.html.jinja')
