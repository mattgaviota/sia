# coding=utf-8
"""Modelo de base de datos en el formato definido por pyDAL"""
from pydal import DAL, Field


USUARIO = 'admin'
PASSW = 'Digio123'
SERVIDOR = '192.168.0.8'
BASE = 'digiomanager'

DB = DAL(
    "postgres://{0}:{1}@{2}/{3}".format(USUARIO, PASSW, SERVIDOR, BASE),
    pool_size=10,
    ignore_field_case=False,
    entity_quoting=True
)

MIGRATE = False

DB.define_table(
    'accesos',
    Field('id', type='id'),
    Field('name', type='string', length=100),
    Field('username', type='string', length=50),
    Field('password', type='string', length=50),
    Field('created_at', type='datetime'),
    Field('updated_at', type='datetime'),
    migrate=MIGRATE
)

DB.define_table(
    'comandos',
    Field('id', type='id'),
    Field('name', type='string', length=20),
    Field('options', type='string', length=150),
    Field('title', type='string', length=150),
    Field('need_sudo', type='boolean', default=False),
    Field('created_at', type='datetime'),
    Field('updated_at', type='datetime'),
    migrate=MIGRATE
)

DB.define_table(
    'establecimientos',
    Field('id', type='id'),
    Field('name', type='string', length=100, unique=True),
    Field('ip', type='string', length=20),
    Field('port', type='string', length=5),
    Field('dbname', type='string', length=50),
    Field('db_dest', type='string', length=50),
    Field('id_establecimiento_destino', type='reference establecimientos'),
    Field('id_acceso', type='reference accesos'),
    Field('created_at', type='datetime'),
    Field('updated_at', type='datetime'),
    migrate=MIGRATE
)

DB.define_table(
    'folders',
    Field('id', type='id'),
    Field('name', type='string', length=50, unique=True),
    Field('path', type='string', length=150),
    Field('latest', type='boolean', default=True),
    Field('created_at', type='datetime'),
    migrate=MIGRATE
)

DB.define_table(
    'files',
    Field('id', type='id'),
    Field('name', type='string', length=50, unique=True),
    Field('filename', type='string', length=100, unique=True),
    Field('filesize', type='integer'),
    Field('id_folder', type='reference folders'),
    Field('created_at', type='datetime'),
    migrate=MIGRATE
)

DB.define_table(
    'revisions',
    Field('id', type='id'),
    Field('id_user', type='reference users'),
    Field('id_comando', type='reference comandos'),
    Field('comentario', type='string', length=150),
    Field('created_at', type='datetime'),
    migrate=MIGRATE
)

DB.define_table(
    'servidores',
    Field('id', type='id'),
    Field('name', type='string', length=100),
    Field('host', type='string', length=150, unique=True),
    Field('port', type='string', length=5, unique=True),
    Field('id_acceso', type='reference accesos'),
    Field('last_access', type='datetime'),
    Field('created_at', type='datetime'),
    Field('updated_at', type='datetime'),
    migrate=MIGRATE
)

DB.define_table(
    'types',
    Field('id', type='id'),
    Field('name', type='string', length=50),
    Field('modelo', rname='class', type='string', length=50),
    Field('prefijo', type='string', length=5, unique=True),
    Field('created_at', type='datetime'),
    Field('updated_at', type='datetime'),
    migrate=MIGRATE
)

DB.define_table(
    'users',
    Field('id', type='id'),
    Field('name', type='string', length=40),
    Field('last_name', type='string', length=40),
    Field('login', type='string', length=40, unique=True),
    Field('password', type='string', length=128),
    Field('is_admin', type='boolean', default=False),
    Field('is_client', type='boolean', default=False),
    Field('created_at', type='datetime'),
    Field('updated_at', type='datetime'),
    migrate=MIGRATE
)
