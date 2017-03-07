# coding=utf-8
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from ..forms import Servidor_form, Acceso_form
from ..modelos.servidores import Servidores
from ..modelos.accesos import Accesos


admin = Blueprint(
    'admin',
    __name__,
    template_folder='templates'
)


@admin.route('/')
@login_required
def index():
    """admin page"""
    return render_template('main.html.jinja')


@admin.route('/list')
def list():
    """ Listar establecimientos. """
    databases = Servidores().get_servidores()
    return render_template(
        'databases/list.html.jinja',
        databases=databases
    )


@admin.route('/create')
def create():
    """ Formulario de creacion de un establecimiento. """
    databases = Servidores().get_servidores()
    form = Servidor_form()
    form.id_acceso.choices = [(0, 'Ninguno')] + [
        (ac['id'], ac['name']) for ac in Accesos().get_accesos()
    ]
    form.id_servidor_destino.choices = [(0, 'Ninguno')] + [
        (ser['id'], ser['name']) for ser in Servidores().get_servidores()
    ]
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
    form.id_acceso.choices = [(0, 'Ninguno')] + [
        (ac['id'], ac['name']) for ac in Accesos().get_accesos()
    ]
    form.id_servidor_destino.choices = [(0, 'Ninguno')] + [
        (ser['id'], ser['name']) for ser in Servidores().get_servidores()
    ]
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


@admin.route('/edit/<id_servidor>')
def edit(id_servidor):
    """ Muestra los datos del hospital para editarlos. """
    databases = Servidores().get_servidores()
    datos = Servidores().get_servidor(id_servidor)
    form = Servidor_form(**datos)
    form.id_acceso.choices = [(0, 'Ninguno')] + [
        (ac['id'], ac['name']) for ac in Accesos().get_accesos()
    ]
    form.id_servidor_destino.choices = [(0, 'Ninguno')] + [
        (ser['id'], ser['name']) for ser in Servidores().get_servidores()
    ]
    return render_template(
        'databases/edit.html.jinja',
        form=form,
        databases=databases,
        active=id_servidor
    )


@admin.route('/update', methods=['POST'])
def update():
    """ Actualiza los datos de un establecimiento. """
    form = Servidor_form()
    form.id_acceso.choices = [(0, 'Ninguno')] + [
        (ac['id'], ac['name']) for ac in Accesos().get_accesos()
    ]
    form.id_servidor_destino.choices = [(0, 'Ninguno')] + [
        (ser['id'], ser['name']) for ser in Servidores().get_servidores()
    ]
    if form.validate_on_submit():
        if Servidores().update_servidor(form):
            flash('El establecimiento se actualizó correctamente.', 'success')
        else:
            flash('Hubo un error al actualizar el establecimiento', 'error')
    return redirect(url_for('admin.edit', id_servidor=form.id.data))


@admin.route('/delete/<id_servidor>')
def delete(id_servidor):
    """ Eliminar establecimiento. """
    if Servidores().delete(id_servidor):
        flash('El establecimiento se eliminó correctamente.', 'success')
    else:
        flash('Hubo un error al eliminar el establecimiento', 'error')
    return redirect(url_for('admin.list'))


# Accesos
@admin.route('/listaccess')
def list_access():
    """ Listar datos de accesos a las bases de datos. """
    accesos = Accesos().get_accesos()
    return render_template(
        'access/list.html.jinja',
        accesos=accesos
    )


@admin.route('/createaccess')
def create_access():
    """Formulario de creación de accesos."""
    accesos = Accesos().get_accesos()
    form = Acceso_form()
    return render_template(
        'access/create.html.jinja',
        accesos=accesos,
        form=form
    )


@admin.route('/storeaccess', methods=['POST'])
def store_access():
    """Crear accesos."""
    accesos = Accesos().get_accesos()
    form = Acceso_form()
    if form.validate_on_submit():
        if Accesos().insert_acceso(form):
            flash('El acceso se creó correctamente.', 'success')
        else:
            flash('Hubo un error al guardar', 'error')
        return redirect(url_for('admin.create_access'))
    return render_template(
        'access/create.html.jinja',
        accesos=accesos,
        form=form
    )


@admin.route('/editaccess/<id_acceso>')
def edit_access(id_acceso):
    """Muestra los datos de acceso para editarlos. """
    accesos = Accesos().get_accesos()
    datos = Accesos().get_acceso(id_acceso)
    form = Acceso_form(**datos)
    return render_template(
        'access/edit.html.jinja',
        form=form,
        accesos=accesos,
        active=id_acceso
    )


@admin.route('/updateaccess', methods=['POST'])
def update_access():
    """ Actualiza los datos de acceso a las bases de datos. """
    form = Acceso_form()
    if form.validate_on_submit():
        if Accesos().update_acceso(form):
            flash('El acceso se actualizó correctamente.', 'success')
        else:
            flash('Hubo un error al actualizar el acceso', 'error')
    return redirect(url_for('admin.edit_access', id_acceso=form.id.data))


@admin.route('/deleteaccess/<id_acceso>')
def delete_access(id_acceso):
    """Eliminar acceso."""
    if Accesos().delete(id_acceso):
        flash('El acceso se eliminó correctamente.', 'success')
    else:
        flash('Hubo un error al eliminar el acceso', 'error')
    return redirect(url_for('admin.list_access'))
