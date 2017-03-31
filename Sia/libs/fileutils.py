# coding=utf-8

from datetime import datetime
from ..modelos.folders import Folders
from ..modelos.files import Files
from ..modelos.versiones import Versiones


class Filemanager(object):
    """docstring for Handler."""
    def __init__(self):
        super(Filemanager, self).__init__()

    def get_all_folders(self):
        """ Retorna todas las carpetas. """
        folders = Folders().get_folders()
        return folders

    def get_files_from_folder(self, folder_id):
        """ Retorna todos los archivos de una carpeta. """
        files = Files().get_files_by_folder(folder_id)
        return files

    def get_versiones_disponibles(self):
        versiones = []
        folders = self.get_all_folders()
        if folders:
            versiones_subidas = []
            for folder in folders:
                versiones_subidas.append(folder.versionsistemaid)
                versiones = Versiones().get_versiones(versiones_subidas)
        else:
            versiones = Versiones().get_versiones()
        return versiones

    def upload_files(self, form):
        pass
