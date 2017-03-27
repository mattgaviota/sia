# coding=utf-8
from flask import Blueprint, render_template, request
from flask_login import login_required
from ..libs.revutils import Revisioner


historial = Blueprint(
    'historial',
    __name__,
    template_folder='templates'
)


@historial.route('/')
@login_required
def index():
    """index all revisions"""
    revisiones = Revisioner().get_all_revisions()
    return render_template('historial/index.html.jinja', revisiones=revisiones)

@historial.route('/user/<user_id>')
@login_required
def user(user_id):
    """user revisions"""
    revisiones = Revisioner().get_revisions_by_user(user_id)
    usuario = revisiones[0]['usuario']
    return render_template(
        'historial/user.html.jinja',
        revisiones=revisiones,
        usuario=usuario
    )
