# coding=utf-8
from flask import Blueprint, render_template, request, flash
from flask import redirect, url_for, current_app
from flask_login import login_required
from ..forms import Establecimiento_form, Acceso_form, Servidor_form
from ..modelos.establecimientos import Establecimientos
from ..modelos.accesos import Accesos
from ..modelos.servidores import Servidores
from ..libs import is_admin


admin = Blueprint(
    'admin',
    __name__,
    template_folder='templates'
)


@admin.route('/')
@login_required
@is_admin
def index():
    """admin page"""
    return render_template('main.html.jinja')


# Establecimientos
@admin.route('/establecimientos')
@login_required
@is_admin
def establecimientos_list():
    """ Listar establecimientos. """
    establecimientos = Establecimientos().get_establecimientos()
    return render_template(
        'establecimientos/list.html.jinja',
        establecimientos=establecimientos
    )


@admin.route('/establecimientos/create')
@login_required
@is_admin
def establecimientos_create():
    """ Formulario de creacion de un establecimiento. """
    establecimientos = Establecimientos().get_establecimientos()
    form = Establecimiento_form()
    form.id_acceso.choices = [(0, 'Ninguno')] + [
        (ac['id'], ac['name']) for ac in Accesos().get_accesos()
    ]
    form.id_establecimiento_destino.choices = [(0, 'Ninguno')] + [
        (ser['id'], ser['name']) for ser in Establecimientos().get_establecimientos()
    ]
    return render_template(
        'establecimientos/create.html.jinja',
        establecimientos=establecimientos,
        form=form
    )


@admin.route('/establecimientos/store', methods=['POST'])
@login_required
@is_admin
def establecimientos_store():
    """Crear establecimiento del registro."""
    establecimientos = Establecimientos().get_establecimientos()
    form = Establecimiento_form()
    form.id_acceso.choices = [(0, 'Ninguno')] + [
        (ac['id'], ac['name']) for ac in Accesos().get_accesos()
    ]
    form.id_establecimiento_destino.choices = [(0, 'Ninguno')] + [
        (ser['id'], ser['name']) for ser in Establecimientos().get_establecimientos()
    ]
    if form.validate_on_submit():
        if Establecimientos().insert_establecimiento(form):
            flash('El establecimiento se creó correctamente.', 'success')
        else:
            flash('Hubo un error al guardar', 'error')
        return redirect(url_for('admin.establecimientos_create'))
    return render_template(
        'establecimientos/create.html.jinja',
        establecimientos=establecimientos,
        form=form
    )


@admin.route('/establecimientos/edit/<id_establecimiento>')
@login_required
@is_admin
def establecimientos_edit(id_establecimiento):
    """ Muestra los datos del hospital para editarlos. """
    establecimientos = Establecimientos().get_establecimientos()
    datos = Establecimientos().get_establecimiento(id_establecimiento)
    form = Establecimiento_form(**datos)
    form.id_acceso.choices = [(0, 'Ninguno')] + [
        (ac['id'], ac['name']) for ac in Accesos().get_accesos()
    ]
    form.id_establecimiento_destino.choices = [(0, 'Ninguno')] + [
        (ser['id'], ser['name']) for ser in Establecimientos().get_establecimientos()
    ]
    return render_template(
        'establecimientos/edit.html.jinja',
        form=form,
        establecimientos=establecimientos,
        active=id_establecimiento
    )


@admin.route('/establecimientos/update', methods=['POST'])
@login_required
@is_admin
def establecimientos_update():
    """ Actualiza los datos de un establecimiento. """
    form = Establecimiento_form()
    form.id_acceso.choices = [(0, 'Ninguno')] + [
        (ac['id'], ac['name']) for ac in Accesos().get_accesos()
    ]
    form.id_establecimiento_destino.choices = [(0, 'Ninguno')] + [
        (ser['id'], ser['name']) for ser in Establecimientos().get_establecimientos()
    ]
    if form.validate_on_submit():
        if Establecimientos().update_establecimiento(form):
            flash('El establecimiento se actualizó correctamente.', 'success')
        else:
            flash('Hubo un error al actualizar el establecimiento', 'error')
    return redirect(
        url_for('admin.establecimientos_edit', id_establecimiento=form.id.data)
    )


@admin.route('/establecimientos/delete/<id_establecimiento>')
@login_required
@is_admin
def establecimientos_delete(id_establecimiento):
    """ Eliminar establecimiento. """
    if Establecimientos().delete(id_establecimiento):
        flash('El establecimiento se eliminó correctamente.', 'success')
    else:
        flash('Hubo un error al eliminar el establecimiento', 'error')
    return redirect(url_for('admin.establecimientos_list'))


# Accesos
@admin.route('/accesos')
@login_required
@is_admin
def accesos_list():
    """ Listar datos de accesos a las bases de datos. """
    accesos = Accesos().get_accesos()
    return render_template(
        'access/list.html.jinja',
        accesos=accesos
    )


@admin.route('/accesos/create')
@login_required
@is_admin
def accesos_create():
    """Formulario de creación de accesos."""
    accesos = Accesos().get_accesos()
    form = Acceso_form()
    return render_template(
        'access/create.html.jinja',
        accesos=accesos,
        form=form
    )


@admin.route('/accesos/store', methods=['POST'])
@login_required
@is_admin
def accesos_store():
    """Crear accesos."""
    accesos = Accesos().get_accesos()
    form = Acceso_form()
    if form.validate_on_submit():
        if Accesos().insert_acceso(form):
            flash('El acceso se creó correctamente.', 'success')
        else:
            flash('Hubo un error al guardar', 'error')
        return redirect(url_for('admin.accesos_create'))
    return render_template(
        'access/create.html.jinja',
        accesos=accesos,
        form=form
    )


@admin.route('/accesos/edit/<id_acceso>')
@login_required
@is_admin
def accesos_edit(id_acceso):
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


@admin.route('/accesos/update', methods=['POST'])
@login_required
@is_admin
def accesos_update():
    """ Actualiza los datos de acceso a las bases de datos. """
    form = Acceso_form()
    if form.validate_on_submit():
        if Accesos().update_acceso(form):
            flash('El acceso se actualizó correctamente.', 'success')
        else:
            flash('Hubo un error al actualizar el acceso', 'error')
    return redirect(url_for('admin.accesos_edit', id_acceso=form.id.data))


@admin.route('/accesos/delete/<id_acceso>')
@login_required
@is_admin
def accesos_delete(id_acceso):
    """Eliminar acceso."""
    if Accesos().delete(id_acceso):
        flash('El acceso se eliminó correctamente.', 'success')
    else:
        flash('Hubo un error al eliminar el acceso', 'error')
    return redirect(url_for('admin.accesos_list'))


# Servidores
@admin.route('/servidores')
@login_required
@is_admin
def servidores_list():
    """ Listar servidores. """
    servidores = Servidores().get_servidores()
    return render_template(
        'servidores/list.html.jinja',
        servidores=servidores
    )


@admin.route('/servidores/create')
@login_required
@is_admin
def servidores_create():
    """ Formulario de creacion de un servidor. """
    servidores = Servidores().get_servidores()
    form = Servidor_form()
    form.id_acceso.choices = [(0, 'Ninguno')] + [
        (ac['id'], ac['name']) for ac in Accesos().get_accesos()
    ]
    return render_template(
        'servidores/create.html.jinja',
        servidores=servidores,
        form=form
    )


@admin.route('/servidores/store', methods=['POST'])
@login_required
@is_admin
def servidores_store():
    """Crear servidor del registro."""
    servidores = Servidores().get_servidores()
    form = Servidor_form()
    form.id_acceso.choices = [(0, 'Ninguno')] + [
        (ac['id'], ac['name']) for ac in Accesos().get_accesos()
    ]
    if form.validate_on_submit():
        if Servidores().insert_servidor(form):
            flash('El servidor se creó correctamente.', 'success')
        else:
            flash('Hubo un error al guardar', 'error')
        return redirect(url_for('admin.servidores_create'))
    return render_template(
        'servidores/create.html.jinja',
        servidores=servidores,
        form=form
    )


@admin.route('/servidores/edit/<id_servidor>')
@login_required
@is_admin
def servidores_edit(id_servidor):
    """ Muestra los datos del hospital para editarlos. """
    servidores = Servidores().get_servidores()
    datos = Servidores().get_servidor(id_servidor)
    form = Servidor_form(**datos)
    form.id_acceso.choices = [(0, 'Ninguno')] + [
        (ac['id'], ac['name']) for ac in Accesos().get_accesos()
    ]
    return render_template(
        'servidores/edit.html.jinja',
        form=form,
        servidores=servidores,
        active=id_servidor
    )


@admin.route('/servidores/update', methods=['POST'])
@login_required
@is_admin
def servidores_update():
    """ Actualiza los datos de un servidor. """
    form = Servidor_form()
    form.id_acceso.choices = [(0, 'Ninguno')] + [
        (ac['id'], ac['name']) for ac in Accesos().get_accesos()
    ]
    if form.validate_on_submit():
        if Servidores().update_servidor(form):
            flash('El servidor se actualizó correctamente.', 'success')
        else:
            flash('Hubo un error al actualizar el servidor', 'error')
    return redirect(url_for('admin.servidores_edit', id_servidor=form.id.data))


@admin.route('/servidores/delete/<id_servidor>')
@login_required
@is_admin
def servidores_delete(id_servidor):
    """ Eliminar servidor. """
    if Servidores().delete(id_servidor):
        flash('El servidor se eliminó correctamente.', 'success')
    else:
        flash('Hubo un error al eliminar el servidor', 'error')
    return redirect(url_for('admin.servidores_list'))
