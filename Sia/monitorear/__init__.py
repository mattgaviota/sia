# coding=utf-8
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from ..libs import is_not_consulta
from ..libs.srvutils import Runner
from ..libs.revutils import Revisioner
from ..forms import Servidor_form
from ..modelos.servidores import Servidores
from ..modelos.comandos import Comandos


monitorear = Blueprint(
    'monitorear',
    __name__,
    template_folder='templates'
)


@monitorear.route('/')
@login_required
@is_not_consulta
def index():
    """index"""
    servidores = Servidores().get_servidores()
    return render_template('monitorear/index.html.jinja', servidores=servidores)


@monitorear.route('/chequear/<id_servidor>')
@login_required
@is_not_consulta
def check(id_servidor):
    """Muestra los datos del hospital"""
    servidores = Servidores().get_servidores()
    datos = Servidores().get_servidor(id_servidor)
    comandos = Comandos().get_comandos()
    return render_template(
        'monitorear/check.html.jinja',
        servidores=servidores,
        comandos=comandos,
        active_servidor=int(id_servidor)
    )

@monitorear.route('/ejecutar/<id_servidor>/<id_comando>')
@login_required
@is_not_consulta
def ejecutar(id_servidor, id_comando):
    """ejecutar comando"""
    servidores = Servidores().get_servidores()
    servidor = Servidores().get_servidor(id_servidor)
    comandos = Comandos().get_comandos()
    comando = Comandos().get_comando(id_comando)
    result = Runner(comando, servidor).run()
    Revisioner(user=current_user, comando=comando).save_revision(
        'en el servidor {}'.format(servidor.name)
    )
    return render_template(
        'monitorear/ejecutar.html.jinja',
        servidores=servidores,
        servidor=servidor,
        comandos=comandos,
        comando=comando,
        result=result,
        active_servidor=int(id_servidor),
        active_comando=int(id_comando)
    )
