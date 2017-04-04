# coding=utf-8

from datetime import datetime
import os
from flask import current_app, jsonify
from werkzeug.utils import secure_filename
from ..modelos.folders import Folders
from ..modelos.files import Files


ALLOWED_EXTENSIONS = set(['sql', 'tgz', 'gz', 'tar', 'pdf'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class Filemanager(object):
    """docstring for Handler."""
    def __init__(self):
        super(Filemanager, self).__init__()
        self.upload_path = current_app.config['UPLOAD_PATH']

    def get_all_folders(self):
        """ Retorna todas las carpetas. """
        folders = Folders().get_folders()
        return folders

    def get_files_from_folder(self, folder_id):
        """ Retorna todos los archivos de una carpeta. """
        files = Files().get_files_by_folder(folder_id)
        return files

    def get_folder(self, folder_id):
        """ Retorna el nombre de la carpeta """
        folder = Folders().get_folder(folder_id)
        return folder.name

    def create_version(self, form):
        """ Crea una carpeta con el numero de versión y
            carga la nueva versión. """
        data = form.data
        reg_folder = {'name': data['version_name']}
        new_path = self.make_folder(reg_folder)
        if new_path:
            reg_folder['path'] = new_path
            if Folders().insert_folder(reg_folder):
                return 1
        return 0

    def make_folder(self, reg_folder):
        newpath = os.path.join(self.upload_path, reg_folder['name'])
        try:
            os.mkdir(newpath)
            return newpath
        except FileExistsError:
            return 0

    def upload_files(self, file, folder_id):
        files = []
        reg_file = {}
        filename = secure_filename(file.filename)
        path = Folders().get_folder(folder_id).path
        file_path = os.path.join(path, filename)
        file.save(file_path)
        f = {'name': filename}
        files.append(f)
        reg_file['name'] = filename
        reg_file['filename'] = filename
        reg_file['id_folder'] = folder_id
        reg_file['filesize'] = os.stat(file_path).st_size
        Files().insert_file(reg_file)
        return jsonify(files=files)

    def delete_folder(self, folder_id):
        folder = Folders().get_folder(folder_id)
        Folders().delete(folder_id)
        try:
            os.rmdir(folder.path)
        except OSError:
            pass

    def delete_file(self, file):
        path = Folders().get_folder(file.id_folder).path
        Files().delete(file.id)
        try:
            os.remove(os.path.join(path, file.filename))
        except OSError:
            pass
