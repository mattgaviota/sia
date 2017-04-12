# coding=utf-8
"""Modelo de base de datos en el formato definido por pyDAL"""
from datetime import datetime
from pydal import DAL, Field
from psycopg2 import IntegrityError

USUARIO = 'postgres'
PASSW = 'Digio123'
SERVIDOR = '192.168.0.120'
BASE = 'datacenter'

DB = DAL(
    "postgres://{0}:{1}@{2}/{3}".format(USUARIO, PASSW, SERVIDOR, BASE),
    pool_size=10,
    ignore_field_case=False,
    entity_quoting=True
)

MIGRATE = False

DB.define_table(
    'vista_consolidados_estadisticas_2',
    Field('contematica', type='string'),
    Field('conestablecimientoid', type='integer'),
    Field('conestablecimientonombre', type='string', length=60),
    Field('concantidad', type='bigint'),
    Field('confecultconsolidacion', type='datetime'),
    migrate=MIGRATE
)

DB.define_table(
    'vista_consolidados_backups_2',
    Field('establecimientonombre', type='string', length=60),
    Field('establecimientoid', type='integer'),
    Field('backupid', type='integer'),
    Field('bakcupestado', type='string', length=100),
    Field('backupfecha', type='datetime'),
    migrate=MIGRATE
)


class Consolidacion(object):

    def __init__(self):
        self.db = DB

    def count_estadisticas(self):
        rows = self.db(self.db.vista_consolidados_estadisticas_2.id > 0).count()
        return rows

    def count_backups(self):
        rows = self.db(self.db.vista_consolidados_backups_2.id > 0).count()
        return rows

    def get_estadisticas_for_page(self, page, per_page):
        min = (page - 1) * per_page
        max = page * per_page
        rows = self.db().select(
            self.db.vista_consolidados_estadisticas_2.ALL,
            limitby=(min, max)
        )
        return rows

    def get_backups_for_page(self, page, per_page):
        min = (page - 1) * per_page
        max = page * per_page
        rows = self.db().select(
            self.db.vista_consolidados_backups_2.ALL,
            limitby=(min, max)
        )
        return rows
