# coding=utf-8
from flask import Blueprint, render_template
from flask import request, flash, redirect, url_for
from flask_login import login_required, current_user
from ..forms import Upload_form
from ..libs import is_admin
from ..libs.fileutils import Filemanager, allowed_file
from ..libs.revutils import Revisioner


versiones = Blueprint(
    'versiones',
    __name__,
    template_folder='templates'
)


@versiones.route('/')
@login_required
def index():
    """index all versions"""
    folders = Filemanager().get_all_folders()
    return render_template('versiones/index.html.jinja', folders=folders)

@versiones.route('/files/<folder_id>')
@login_required
def files(folder_id):
    """index all versions"""
    files = Filemanager().get_files_from_folder(folder_id)
    return render_template(
        'versiones/list.html.jinja',
        files=files,
        folder=Filemanager().get_folder(folder_id),
        folder_id=folder_id
    )

@versiones.route('/uploadfolder', methods=['GET', 'POST'])
@login_required
@is_admin
def upload_folder():
    """ Upload versions(folders). """
    form = Upload_form()
    form.version.choices = [
        (ver['versionsistemaid'], ver['versionsistemadesc'])
        for ver in Filemanager().get_versiones_disponibles()
    ]
    if form.validate_on_submit():
        if Filemanager().create_version(form):
            Revisioner(user=current_user).save_revision(
                'Subió una nueva versión del sistema'
            )
            flash('La versión se creó correctamente.', 'success')
            return redirect(url_for('versiones.index'))
        flash('Hubo un error al crear la versión.', 'error')
        return redirect(url_for('versiones.index'))
    return render_template('versiones/uploadfolder.html.jinja', form=form)

@versiones.route('/uploadfile/<folder_id>', methods=['GET', 'POST'])
@login_required
@is_admin
def upload_file(folder_id):
    """ upload files to a folder. """
    if request.method == 'POST':
        files = []
        file = request.files['file']
        if file and allowed_file(file.filename):
            return Filemanager().upload_files(file, folder_id)
        flash('El archivo no corresponde con los formatos aceptados', 'error')
        return redirect(url_for('versiones.index'))
    return render_template(
        'versiones/uploadfile.html.jinja',
        folder=Filemanager().get_folder(folder_id),
        folder_id=folder_id
    )
