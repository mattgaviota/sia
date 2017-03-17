# coding=utf-8
from flask import Blueprint, render_template, request
from ..libs.dbutils import Handler
from ..forms import Establecimiento_form
from ..modelos.establecimientos import Establecimientos


restaurar = Blueprint(
    'restaurar',
    __name__,
    template_folder='templates'
)


@restaurar.route('/')
def index():
    """index"""
    establecimientos = Establecimientos().get_establecimientos()
    return render_template('restaurar/index.html.jinja', establecimientos=establecimientos)


@restaurar.route('/chequear/<id_establecimiento>')
def check(id_establecimiento):
    """Muestra los datos del hospital"""
    establecimientos = Establecimientos().get_establecimientos()
    datos = Establecimientos().get_establecimiento(id_establecimiento)
    datos['db_clean'] = False
    form = Establecimiento_form(**datos)
    return render_template(
        'restaurar/check.html.jinja',
        form=form,
        establecimientos=establecimientos,
        active=int(id_establecimiento)
    )


@restaurar.route('/validar', methods=['POST'])
def validate():
    """Llama al script que valida la restauración. """
    establecimientos = Establecimientos().get_establecimientos()
    form = Establecimiento_form()
    data = form.data
    if not data['clean_db']:
        del form.clean_db
    del form.id_acceso
    del form.id_establecimiento_destino
    if form.validate_on_submit():
        srv_origen = Establecimientos().get_establecimiento(form.id.data)
        srv_destino = Establecimientos().get_establecimiento(srv_origen.id_establecimiento_destino)
        pasos = Handler(srv_origen, srv_destino, form).validar_script()
    return render_template(
        'restaurar/result.html.jinja',
        form=form,
        establecimientos=establecimientos,
        pasos=pasos,
        active=srv_origen.id
    )


@restaurar.route('/restaurar', methods=['POST'])
def restore():
    """Llama al script que realiza la restauración. """
    establecimientos = Establecimientos().get_establecimientos()
    form = Establecimiento_form()
    srv_origen = Establecimientos().get_establecimiento(form.id.data)
    srv_destino = Establecimientos().get_establecimiento(srv_origen.id_establecimiento_destino)
    result = Handler(srv_origen, srv_destino, form).restaurar_db()
    return render_template(
        'restaurar/output.html.jinja',
        form=form,
        establecimientos=establecimientos,
        pasos=result
    )
