# coding=utf-8
from .modelo import DB
from psycopg2 import IntegrityError
from datetime import datetime


class Establecimientos(object):

    def __init__(self):
        self.db = DB
        self.guarded = ['id', 'clean_db', 'csrf_token']
        self.restricted = ['id_acceso', 'id_establecimiento_destino']

    def get_establecimientos(self):
        rows = self.db(self.db.establecimientos.id > 0).select(
            orderby=self.db.establecimientos.name,
            cacheable=True
        )
        return rows

    def get_establecimiento(self, id):
        row = self.db(self.db.establecimientos.id == id).select().first()
        return row

    def clean_data(self, data):
        data = data.data
        for field in self.guarded:
            data.pop(field)
        for field in self.restricted:
            if not data[field]:
                data.pop(field)
        return data

    def insert_servidor(self, data):
        data = self.clean_data(data)
        data['created_at'] = datetime.now()
        data['updated_at'] = datetime.now()
        id_establecimiento = None
        try:
            id_establecimiento = self.db.establecimientos.insert(**data)
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
        return id_establecimiento

    def update_establecimiento(self, data):
        id_establecimiento = data.id.data
        data = self.clean_data(data)
        data['updated_at'] = datetime.now()
        result = 0
        try:
            self.db(self.db.establecimientos.id == id_establecimiento).update(**data)
            self.db.commit()
            result = 1
        except IntegrityError:
            self.db.rollback()
        return result


    def delete(self, id):
        result = 0
        try:
            self.db(self.db.establecimientos.id == id).delete()
            self.db.commit()
            result = 1
        except IntegrityError:
            self.db.rollback()
        return result
