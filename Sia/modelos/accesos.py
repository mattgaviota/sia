# coding=utf-8
from .modelo import DB
from psycopg2 import IntegrityError
from datetime import datetime


class Accesos(object):

    def __init__(self):
        self.db = DB
        self.guarded = ['id', 'csrf_token']

    def clean_data(self, data):
        data = data.data
        for field in self.guarded:
            data.pop(field)
        return data

    def get_accesos(self):
        rows = self.db(self.db.accesos.id > 0).select(
            orderby=self.db.accesos.name,
            cacheable=True
        )
        return rows

    def get_acceso(self, id):
        row = self.db(self.db.accesos.id == id).select().first()
        return row

    def insert_acceso(self, data):
        data = self.clean_data(data)
        data['created_at'] = datetime.now()
        data['updated_at'] = datetime.now()
        id_acceso = None
        try:
            id_acceso = self.db.accesos.insert(**data)
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
        return id_acceso

    def update_acceso(self, data):
        id_acceso = data.id.data
        data = self.clean_data(data)
        data['updated_at'] = datetime.now()
        result = 0
        try:
            self.db(self.db.accesos.id == id_acceso).update(**data)
            self.db.commit()
            result = 1
        except IntegrityError:
            self.db.rollback()
        return result

    def delete(self, id):
        result = 0
        try:
            self.db(self.db.accesos.id == id).delete()
            self.db.commit()
            result = 1
        except IntegrityError:
            self.db.rollback()
        return result
