# coding=utf-8
from flask import Blueprint, render_template, request
from ..lib.dbutils import Handler
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
    datos = Servidores().get_servidor(id_servidor)
    datos['db_clean'] = False
    form = Servidor_form(**datos)
    return render_template(
        'restaurar/check.html.jinja',
        form=form,
        databases=databases,
        active=id_servidor
    )


@restaurar.route('/validar', methods=['POST'])
def validate():
    """Llama al script que valida la restauración. """
    databases = Servidores().get_servidores()
    form = Servidor_form()
    data = form.data
    if not data['clean_db']:
        del form.clean_db
    del form.id_acceso
    del form.id_servidor_destino
    if form.validate_on_submit():
        srv_origen = Servidores().get_servidor(form.id.data)
        srv_destino = Servidores().get_servidor(srv_origen.id_servidor_destino)
        pasos = Handler(srv_origen, srv_destino, form).validar_script()
    return render_template(
        'restaurar/result.html.jinja',
        form=form,
        databases=databases,
        pasos=pasos,
        active=srv_origen.id
    )


@restaurar.route('/restaurar', methods=['POST'])
def restore():
    """Llama al script que realiza la restauración. """
    databases = Servidores().get_servidores()
    form = Servidor_form()
    srv_origen = Servidores().get_servidor(form.id.data)
    srv_destino = Servidores().get_servidor(srv_origen.id_servidor_destino)
    result = Handler(srv_origen, srv_destino, form).restaurar_db()
    return render_template(
        'restaurar/output.html.jinja',
        form=form,
        databases=databases,
        pasos=result
    )
