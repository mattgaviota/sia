# coding=utf-8
from .modelo import DB
from psycopg2 import IntegrityError
from datetime import datetime


class Servidores(object):

    def __init__(self):
        self.db = DB
        self.guarded = ['id', 'csrf_token']

    def get_servidores(self):
        rows = self.db(self.db.servidores.id > 0).select(
            orderby=self.db.servidores.name,
            cacheable=True
        )
        return rows

    def get_servidor(self, id):
        row = self.db(self.db.servidores.id == id).select().first()
        return row

    def clean_data(self, data):
        data = data.data
        for field in self.guarded:
            data.pop(field)
        return data

    def insert_servidor(self, data):
        data = self.clean_data(data)
        data['created_at'] = datetime.now()
        data['updated_at'] = datetime.now()
        id_servidor = None
        try:
            id_servidor = self.db.servidores.insert(**data)
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
        return id_servidor

    def update_last_access(self, id_servidor):
        result = 0
        try:
            self.db(self.db.servidores.id == id_servidor).update(
                **{'last_access': datetime.now()}
            )
            self.db.commit()
            result = 1
        except IntegrityError:
            self.db.rollback()
        return result

    def update_servidor(self, data):
        id_servidor = data.id.data
        data = self.clean_data(data)
        data['updated_at'] = datetime.now()
        result = 0
        try:
            self.db(self.db.servidores.id == id_servidor).update(**data)
            self.db.commit()
            result = 1
        except IntegrityError:
            self.db.rollback()
        return result

    def delete(self, id):
        result = 0
        try:
            self.db(self.db.servidores.id == id).delete()
            self.db.commit()
            result = 1
        except IntegrityError:
            self.db.rollback()
        return result
