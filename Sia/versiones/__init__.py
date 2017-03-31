# coding=utf-8
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from ..forms import Upload_form
from ..libs import is_admin
from ..libs.fileutils import Filemanager
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
    return render_template('versiones/list.html.jinja', files=files)

@versiones.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    """index all versions"""
    form = Upload_form()
    form.version.choices = [
        (ver['versionsistemaid'], ver['versionsistemadesc'])
        for ver in Filemanager().get_versiones_disponibles()
    ]
    if form.validate_on_submit():
        Filemanager().upload_files(form)
        Revisioner(user=current_user).save_revision(
            'Subió una nueva versión del sistema'
        )
        flash('Ha ingresado correctamente.', 'success')
        return redirect(url_for('home.index'))
    return render_template('versiones/upload.html.jinja', form=form)
