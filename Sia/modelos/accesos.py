# coding=utf-8
from .modelo import DB
from psycopg2 import IntegrityError
from datetime import datetime


class Accesos(object):

    def __init__(self):
        self.db = DB

    def get_accesos(self):
        rows = self.db(self.db.accesos.id > 0).select()
        return rows

    def get_acceso(self, id):
        row = self.db(self.db.acceso.id == id).select().first()
        return row

    def insert_acceso(self, data):
        data['created_at'] = datetime.now()
        data['updated_at'] = datetime.now()
        try:
            id_acceso = self.db.accesos.insert(**data)
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
        return id_acceso

    def update_acceso(self, data, id):
        data['updated_at'] = datetime.now()
        try:
            self.db(self.db.accesos.id == id).update(**data)
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
