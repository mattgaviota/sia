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
    'servidores',
    Field('id', type='id'),
    Field('name', type='string', length=100, unique=True),
    Field('ip', type='string', length=20),
    Field('port', type='string', length=5),
    Field('dbname', type='string', length=50),
    Field('db_dest', type='string', length=50),
    Field('id_servidor_destino', type='reference servidores'),
    Field('id_acceso', type='reference accesos'),
    Field('created_at', type='datetime'),
    Field('updated_at', type='datetime'),
    migrate=MIGRATE
)

DB.define_table(
    'users',
    Field('id', type='id'),
    Field('name', type='string', length=40),
    Field('last_name', type='string', length=40),
    Field('login', type='string', length=40),
    Field('password', type='string', length=128),
    Field('is_admin', type='boolean', default=False),
    Field('created_at', type='datetime'),
    Field('updated_at', type='datetime'),
    migrate=MIGRATE
)
