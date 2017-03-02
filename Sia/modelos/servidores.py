# coding=utf-8
from .modelo import DB
from psycopg2 import IntegrityError
from datetime import datetime


class Servidores(object):

    def __init__(self):
        self.db = DB
        self.guarded = ['id', 'clean_db', 'csrf_token']
        self.restricted = ['id_acceso', 'id_servidor_destino']

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
        for field in self.restricted:
            if not data[field]:
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

    def get_acceso_servidor(self, id):
        row = self.db(self.db.accesos_servidores.id_servidor == id).select(
            self.db.accesos_servidores.id_acceso
        ).first()
        acceso = self.db(self.db.accesos.id == row.id_acceso).select(
            self.db.accesos.username,
            self.db.accesos.password
        ).first()
        return acceso

    def delete(self, id):
        result = 0
        try:
            self.db(self.db.servidores.id == id).delete()
            self.db.commit()
            result = 1
        except IntegrityError:
            self.db.rollback()
        return result
