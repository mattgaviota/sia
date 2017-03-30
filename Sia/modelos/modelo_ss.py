# coding=utf-8
"""Modelo de base de datos en el formato definido por pyDAL"""
from pydal import DAL, Field


USUARIO = 'postgres'
PASSW = 'Digio123'
SERVIDOR = '192.168.0.110'
BASE = 'desarrollo'

DB = DAL(
    "postgres://{0}:{1}@{2}/{3}".format(USUARIO, PASSW, SERVIDOR, BASE),
    pool_size=10,
    ignore_field_case=False,
    entity_quoting=True
)

MIGRATE = False

DB.define_table(
    'seg_versionsistema',
    Field('versionsistemaid', type='id'),
    Field('versionsistemadesc', type='string', length=10),
    Field('versionsistemafecha', type='date'),
    Field('versionsistemausumod', type='integer'),
    Field('versionsistemausubaja', type='integer'),
    Field('versionsistemafechamod', type='date'),
    Field('versionsistemafechabaja', type='date'),
    migrate=MIGRATE
)

DB.define_table(
    'seg_versionsistemadetalle',
    Field('versionsistemadetalleid', type='id'),
    Field('versionsistemaid', type='reference seg_versionsistema'),
    Field('versionsistemadetalledesc', type='string', length=1000),
    Field('versionsistemadetalleusumod', type='integer'),
    Field('versionsistemadetalleusubaja', type='integer'),
    Field('versionsistemadetallefechamod', type='date'),
    Field('versionsistemadetallefechabaja', type='date'),
    migrate=MIGRATE
)
