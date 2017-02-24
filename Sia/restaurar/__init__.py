# coding=utf-8
from flask import Blueprint, render_template, request
from ..dbutils import Handler
from ..forms import Servidor_form
from ..modelos.servidores import Servidores


restaurar = Blueprint(
    'restaurar',
    __name__,
    template_folder='templates'
)


@restaurar.route('/')
def index():
    """index"""
    databases = Servidores().get_servidores()
    return render_template('restaurar/index.html.jinja', databases=databases)


@restaurar.route('/chequear/<id_servidor>')
def check(id_servidor):
    """Muestra los datos del hospital"""
    databases = Servidores().get_servidores()
    form = Servidor_form(databases, db_clean=False)
    return render_template(
        'restaurar/check.html.jinja',
        form=form,
        databases=databases,
        active=hospital
    )


@restaurar.route('/validar', methods=['POST'])
def validate():
    """Llama al script que valida la restauración. """
    databases = Servidores().get_servidores()
    form = Servidor_form()
    pasos = Handler(form).validar_script()
    return render_template(
        'restaurar/result.html.jinja',
        form=form,
        databases=databases,
        pasos=pasos
    )


@restaurar.route('/restaurar', methods=['POST'])
def restore():
    """Llama al script que realiza la restauración. """
    databases = Servidores().get_servidores()
    form = Servidor_form()
    result = Handler(form).restaurar_db()
    return render_template(
        'restaurar/output.html.jinja',
        form=form,
        databases=databases,
        pasos=result
    )
