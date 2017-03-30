# coding=utf-8
from flask import Blueprint, render_template, request
from flask_login import login_required
from ..libs import is_admin
from ..libs.fileutils import Filemanager


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

@versiones.route('/upload')
@login_required
def upload(folder_id):
    """index all versions"""
    return render_template('versiones/list.html.jinja', files=files)
