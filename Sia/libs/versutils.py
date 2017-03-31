# coding=utf-8

from datetime import datetime
from ..modelos.folders import Folders
from ..modelos.versiones import Versiones


class Versionmanager(object):
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
