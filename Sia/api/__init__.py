# coding=utf-8
from flask import Blueprint, Response
from dicttoxml import dicttoxml
from ..libs.fileutils import Filemanager


api = Blueprint(
    'api',
    __name__,
    template_folder='templates'
)


@api.route('/')
def index():
    """index all api endpoints"""
    endpoints = {
        'última versión': '/last_version',
        'versiones': '/versiones',
        'archivos de una version': '/version/<nombre_version>'
    }
    endpoints = dicttoxml(endpoints, attr_type=False)
    return Response(endpoints, mimetype='application/xml')


@api.route('/last_version')
def last_version():
    """ get the last version """
    last_version = Filemanager().get_last_folder()
    version = {
        'nombre': last_version.name,
        'fecha': last_version.created_at.strftime('%d/%m/%Y')
    }
    version = dicttoxml(version, custom_root="version", attr_type=False)
    return Response(version, mimetype='application/xml')


@api.route('/versiones')
def versiones():
    """ get the last version """
    versiones = Filemanager().get_all_folders()
    versiones_xml = {}
    for version in versiones:
        versiones_xml[str(version.id)] = {
            'nombre': version.name,
            'fecha': version.created_at.strftime('%d/%m/%Y')
        }
    versiones_xml = dicttoxml(
        versiones_xml,
        custom_root="versiones",
        attr_type=False
    )
    return Response(versiones_xml, mimetype='application/xml')

@api.route('/version/<name>')
def version(name):
    """ get the files of the version """
    folder = Filemanager().get_folder_by_name(name)
    files = {}
    for file in Filemanager().get_files_from_folder(folder.id):
        files[str(file.id)] = {
            'nombre': file.name,
            'archivo': file.filename,
            'tamaño': '{:.2f} Mb'.format(file.filesize / (1024.0 ** 2)),
            'fecha': file.created_at.strftime('%d/%m/%Y')
        }
    files = dicttoxml(
        files,
        custom_root="archivos",
        attr_type=False
    )
    return Response(files, mimetype='application/xml')
