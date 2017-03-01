# coding=utf-8
from flask import Blueprint, render_template, request, flash, redirect, url_for
from ..forms import Servidor_form, Acceso_form
from ..modelos.servidores import Servidores
from ..modelos.accesos import Accesos


admin = Blueprint(
    'admin',
    __name__,
    template_folder='templates'
)


@admin.route('/')
def index():
    """admin page"""
    return render_template('main.html.jinja')


@admin.route('/listjson')
def list_json():
    """editar json con los hospitales. """
    databases = Servidores().get_servidores()
    return render_template(
        'databases/list.html.jinja',
        databases=databases
    )


@admin.route('/editjson/<id_servidor>')
def edit_json(id_servidor):
    """Muestra los datos del hospital"""
    databases = Servidores().get_servidores()
    datos = Servidores().get_servidor(id_servidor)
    form = Servidor_form(**datos)
    return render_template(
        'databases/edit.html.jinja',
        form=form,
        databases=databases,
        active=id_servidor
    )


@admin.route('/updatejson', methods=['POST'])
def update_json():
    """Actualizar json con los hospitales. """
    databases = Servidores().get_servidores()
    form = Servidor_form()
    if form.validate_on_submit():
        if Servidores().update_servidor(form):
            flash('El establecimiento se actualizó correctamente.', 'success')
        else:
            flash('Hubo un error al actualizar el establecimiento', 'error')
    return redirect(url_for('admin.edit_json', id_servidor=form.id.data))


@admin.route('/delete/<id_servidor>')
def delete(id_servidor):
    """Eliminar establecimiento del registro."""
    databases = Servidores().get_servidores()
    if Servidores().delete(id_servidor):
        flash('El establecimiento se eliminó correctamente.', 'success')
    else:
        flash('Hubo un error al eliminar el establecimiento', 'error')
    return redirect(url_for('admin.list_json'))


@admin.route('/create')
def create():
    """Eliminar establecimiento del registro."""
    databases = Servidores().get_servidores()
    form = Servidor_form()
    return render_template(
        'databases/create.html.jinja',
        databases=databases,
        form=form
    )


@admin.route('/store', methods=['POST'])
def store():
    """Crear establecimiento del registro."""
    databases = Servidores().get_servidores()
    form = Servidor_form()
    if form.validate_on_submit():
        if Servidores().insert_servidor(form):
            flash('El establecimiento se creó correctamente.', 'success')
        else:
            flash('Hubo un error al guardar', 'error')
        return redirect(url_for('admin.create'))
    return render_template(
        'databases/create.html.jinja',
        databases=databases,
        form=form
    )


@admin.route('/listaccess')
def edit_access():
    """ Editar datos de accesos a las bases de datos. """
    accesos = Accesos().get_accesos()
    return render_template(
        'access/list.html.jinja',
        accesos=accesos
    )


@admin.route('/updateaccess', methods=['POST'])
def update_access():
    """ Actuliza los datos de acceso a las bases de datos. """
    access = {}
    access['user'] = request.form['userdb']
    access['password'] = request.form['passw']
    Datautils().update_access(access)
    flash('Los datos de accesos se actualizaron correctamente.')
    return redirect(url_for('admin.edit_access'))
