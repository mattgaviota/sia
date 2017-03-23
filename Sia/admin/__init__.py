# coding=utf-8
from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from ..forms import Establecimiento_form, Acceso_form
from ..forms import Servidor_form, Comando_form
from ..modelos.establecimientos import Establecimientos
from ..modelos.accesos import Accesos
from ..modelos.servidores import Servidores
from ..modelos.comandos import Comandos
from ..libs import is_admin
from ..libs.revutils import Revisioner


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
            Revisioner(user=current_user).save_revision(
                'Creó el estableciemiento {}'.format(form.data['name'])
            )
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
        active=int(id_establecimiento)
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
            Revisioner(user=current_user).save_revision(
                'Actualizó el estableciemiento {}'.format(form.data['name'])
            )
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
    establecimiento = Establecimientos().get_establecimiento(
        id_establecimiento
    )
    if Establecimientos().delete(id_establecimiento):
        Revisioner(user=current_user).save_revision(
            'Eliminó el estableciemiento {}'.format(establecimiento.name)
        )
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
            Revisioner(user=current_user).save_revision(
                'Creó el acceso {}'.format(form.data['name'])
            )
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
        active=int(id_acceso)
    )


@admin.route('/accesos/update', methods=['POST'])
@login_required
@is_admin
def accesos_update():
    """ Actualiza los datos de acceso a las bases de datos. """
    form = Acceso_form()
    if form.validate_on_submit():
        if Accesos().update_acceso(form):
            Revisioner(user=current_user).save_revision(
                'Actualizó el acceso {}'.format(form.data['name'])
            )
            flash('El acceso se actualizó correctamente.', 'success')
        else:
            flash('Hubo un error al actualizar el acceso', 'error')
    return redirect(url_for('admin.accesos_edit', id_acceso=form.id.data))


@admin.route('/accesos/delete/<id_acceso>')
@login_required
@is_admin
def accesos_delete(id_acceso):
    """Eliminar acceso."""
    acceso = Accesos().get_acceso(id_acceso)
    if Accesos().delete(id_acceso):
        Revisioner(user=current_user).save_revision(
            'Eliminó el acceso {}'.format(acceso.name)
        )
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
            Revisioner(user=current_user).save_revision(
                'Creó el servidor {}'.format(form.data['name'])
            )
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
        active=int(id_servidor)
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
            Revisioner(user=current_user).save_revision(
                'Actualizó el servidor {}'.format(form.data['name'])
            )
            flash('El servidor se actualizó correctamente.', 'success')
        else:
            flash('Hubo un error al actualizar el servidor', 'error')
    return redirect(url_for('admin.servidores_edit', id_servidor=form.id.data))


@admin.route('/servidores/delete/<id_servidor>')
@login_required
@is_admin
def servidores_delete(id_servidor):
    """ Eliminar servidor. """
    servidor = Servidores().get_servidor(id_servidor)
    if Servidores().delete(id_servidor):
        Revisioner(user=current_user).save_revision(
            'Eliminó el servidor {}'.format(servidor.name)
        )
        flash('El servidor se eliminó correctamente.', 'success')
    else:
        flash('Hubo un error al eliminar el servidor', 'error')
    return redirect(url_for('admin.servidores_list'))


# Comandos
@admin.route('/comandos')
@login_required
@is_admin
def comandos_list():
    """ Listar datos de comandos. """
    comandos = Comandos().get_comandos()
    return render_template(
        'comandos/list.html.jinja',
        comandos=comandos
    )


@admin.route('/comandos/create')
@login_required
@is_admin
def comandos_create():
    """Formulario de creación de comandos."""
    comandos = Comandos().get_comandos()
    form = Comando_form()
    return render_template(
        'comandos/create.html.jinja',
        comandos=comandos,
        form=form
    )


@admin.route('/comandos/store', methods=['POST'])
@login_required
@is_admin
def comandos_store():
    """Crear comandos."""
    comandos = Comandos().get_comandos()
    form = Comando_form()
    if form.validate_on_submit():
        if Comandos().insert_comando(form):
            Revisioner(user=current_user).save_revision(
                'Creó el comando {}'.format(form.data['title'])
            )
            flash('El comando se creó correctamente.', 'success')
        else:
            flash('Hubo un error al guardar', 'error')
        return redirect(url_for('admin.comandos_create'))
    return render_template(
        'comandos/create.html.jinja',
        comandos=comandos,
        form=form
    )


@admin.route('/comandos/edit/<id_comando>')
@login_required
@is_admin
def comandos_edit(id_comando):
    """Muestra los datos de comando para editarlos. """
    comandos = Comandos().get_comandos()
    datos = Comandos().get_comando(id_comando)
    form = Comando_form(**datos)
    return render_template(
        'comandos/edit.html.jinja',
        form=form,
        comandos=comandos,
        active=int(id_comando)
    )


@admin.route('/comandos/update', methods=['POST'])
@login_required
@is_admin
def comandos_update():
    """ Actualiza los datos de comandos. """
    form = Comando_form()
    if form.validate_on_submit():
        if Comandos().update_comando(form):
            Revisioner(user=current_user).save_revision(
                'Actualizó el acceso {}'.format(form.data['title'])
            )
            flash('El comando se actualizó correctamente.', 'success')
        else:
            flash('Hubo un error al actualizar el comando', 'error')
    return redirect(url_for('admin.comandos_edit', id_comando=form.id.data))


@admin.route('/comandos/delete/<id_comando>')
@login_required
@is_admin
def comandos_delete(id_comando):
    """Eliminar comando."""
    comando = Comandos().get_comando(id_comando)
    if Comandos().delete(id_comando):
        Revisioner(user=current_user).save_revision(
            'Eliminó el comando {}'.format(comando.title)
        )
        flash('El comando se eliminó correctamente.', 'success')
    else:
        flash('Hubo un error al eliminar el comando', 'error')
    return redirect(url_for('admin.comandos_list'))
