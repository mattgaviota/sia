# coding=utf-8
from flask import Blueprint, render_template, current_app
from flask import request, flash, redirect, url_for, jsonify
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
    """index all files"""
    files = Filemanager().get_files_from_folder(folder_id)
    return render_template(
        'versiones/list.html.jinja',
        files=files,
        folder=Filemanager().get_folder(folder_id),
        folder_id=folder_id
    )

@versiones.route('/file/<file_id>')
@login_required
def file(file_id):
    """file options"""
    selected_file = Filemanager().get_file(file_id)
    folder = Filemanager().get_folder(selected_file.id_folder)
    files = Filemanager().get_files_from_folder(folder.id)
    return render_template(
        'versiones/file.html.jinja',
        selected_file=selected_file,
        files=files,
        folder=folder
    )

@versiones.route('/download/<file_id>')
@login_required
def download_file(file_id):
    """download file"""
    return Filemanager().get_file_from_directory(file_id)

@versiones.route('/delete_file/<file_id>')
@login_required
@is_admin
def delete_file(file_id):
    """delete file"""
    selected_file = Filemanager().get_file(file_id)
    Filemanager().delete_file(selected_file)
    flash('Archivo eliminado correctamente.', 'success')
    return redirect(url_for('versiones.files', folder_id=selected_file.id_folder))

@versiones.route('/uploadfolder', methods=['GET', 'POST'])
@login_required
@is_admin
def upload_folder():
    """ Upload versions(folders). """
    form = Upload_form()
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

@versiones.route('/uploadfile/<folder_id>', methods=['POST'])
@login_required
@is_admin
def upload_file(folder_id):
    """ upload files to a folder. """
    if request.method == 'POST':
        files = []
        filename = request.form['name']
        if not filename:
            files.append({'name': 'none', 'error': 'Debe ingresar un nombre.'})
            return jsonify(files=files)
        file = request.files['file']
        if file and allowed_file(file.filename):
            return Filemanager().upload_files(file, filename, folder_id)
        files.append({
            'name': 'none',
            'error': 'El archivo no corresponde con los formatos aceptados'
        })
        return jsonify(files=files)

@versiones.route('/deletefolder/<folder_id>', methods=['GET'])
@login_required
@is_admin
def delete_folder(folder_id):
    """ delete folder and all it's files. """
    files = Filemanager().get_files_from_folder(folder_id)
    for file in files:
        Filemanager().delete_file(file)
    Filemanager().delete_folder(folder_id)
    flash('Versión eliminada juntos con sus archivos.', 'success')
    return redirect(url_for('versiones.index'))

@versiones.route('/latest/<folder_id>', methods=['GET'])
@login_required
@is_admin
def set_latest(folder_id):
    """ Update the version to set the latest """
    Filemanager().set_latest_version(folder_id)
    flash('Versión actualizada correctamente.', 'success')
    return redirect(url_for('versiones.index'))
