# coding=utf-8
from flask import Blueprint, render_template, request

home = Blueprint(
    'home',
    __name__,
    template_folder='templates'
)


@home.route('/')
def index():
    """index"""
    return render_template('index.html.jinja')
