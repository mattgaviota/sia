# coding=utf-8
from flask import Blueprint, render_template, request
from ..libs.dbutils import Handler
from ..forms import Servidor_form
from ..modelos.servidores import Servidores


monitorear = Blueprint(
    'monitorear',
    __name__,
    template_folder='templates'
)


@monitorear.route('/')
def index():
    """index"""
    servidores = Servidores().get_servidores()
    return render_template('monitorear/index.html.jinja', servidores=servidores)


@monitorear.route('/chequear/<id_servidor>')
def check(id_servidor):
    """Muestra los datos del hospital"""
    servidores = Servidores().get_servidores()
    datos = Servidores().get_servidor(id_servidor)
    datos['db_clean'] = False
    form = Servidor_form(**datos)
    return render_template(
        'monitorear/check.html.jinja',
        form=form,
        servidores=servidores,
        active=id_servidor
    )


@monitorear.route('/validar', methods=['POST'])
def validate():
    """Llama al script que valida la restauración. """
    servidores = Servidores().get_servidores()
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
        'monitorear/result.html.jinja',
        form=form,
        servidores=servidores,
        pasos=pasos,
        active=srv_origen.id
    )


@monitorear.route('/monitorear', methods=['POST'])
def restore():
    """Llama al script que realiza la restauración. """
    servidores = Servidores().get_servidores()
    form = Servidor_form()
    srv_origen = Servidores().get_servidor(form.id.data)
    srv_destino = Servidores().get_servidor(srv_origen.id_servidor_destino)
    result = Handler(srv_origen, srv_destino, form).monitorear_db()
    return render_template(
        'monitorear/output.html.jinja',
        form=form,
        servidores=servidores,
        pasos=result
    )
