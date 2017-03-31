# coding=utf-8
from .modelo_ss import DB
from psycopg2 import IntegrityError
from datetime import datetime


class Versiones(object):

    def __init__(self):
        self.db = DB

    def get_versiones(self, versiones_subidas=None):
        if not versiones_subidas:
            rows = self.db(self.db.seg_versionsistema.versionsistemaid > 0).select(
                orderby=~self.db.seg_versionsistema.versionsistemafecha,
                cacheable=True
            )
        else:
            rows = self.db(
                self.db.seg_versionsistema.versionsistemaid.belongs(versiones_subidas)
            ).select(
                orderby=~self.db.seg_versionsistema.versionsistemafecha,
                cacheable=True
            )
        return rows

    def get_version(self, id):
        row = self.db(
            self.db.seg_versionsistema.versionsistemaid == id
        ).select().first()
        return row

    def get_changelog(self, id):
        rows = self.db(
            self.db.seg_versionsistemadetalle.versionsistemaid == id
        ).select(
            orderby=self.db.seg_versionsistema.versionsistemadetalledesc,
            cacheable=True
        )
        return rows
