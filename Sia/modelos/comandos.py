# coding=utf-8
from .modelo import DB
from psycopg2 import IntegrityError, DataError
from datetime import datetime


class Comandos(object):

    def __init__(self):
        self.db = DB
        self.guarded = ['id', 'csrf_token']

    def clean_data(self, data):
        data = data.data
        for field in self.guarded:
            data.pop(field)
        return data

    def get_comandos(self):
        rows = self.db(self.db.comandos.id > 0).select(
            orderby=self.db.comandos.title,
            cacheable=True
        )
        return rows

    def get_comando(self, id):
        row = self.db(self.db.comandos.id == id).select().first()
        return row

    def insert_comando(self, data):
        data = self.clean_data(data)
        data['created_at'] = datetime.now()
        data['updated_at'] = datetime.now()
        id_comando = None
        try:
            id_comando = self.db.comandos.insert(**data)
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
        except DataError:
            self.db.rollback()
        return id_comando

    def update_comando(self, data):
        id_comando = data.id.data
        data = self.clean_data(data)
        data['updated_at'] = datetime.now()
        result = 0
        try:
            self.db(self.db.comandos.id == id_comando).update(**data)
            self.db.commit()
            result = 1
        except IntegrityError:
            self.db.rollback()
        except DataError:
            self.db.rollback()
        return result

    def delete(self, id):
        result = 0
        try:
            self.db(self.db.comandos.id == id).delete()
            self.db.commit()
            result = 1
        except IntegrityError:
            self.db.rollback()
        return result
