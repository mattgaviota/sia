# coding=utf-8
from .modelo import DB
from psycopg2 import IntegrityError
from datetime import datetime


class Servidores(object):

    def __init__(self):
        self.db = DB

    def get_servidores(self):
        rows = self.db(self.db.servidores.id > 0).select()
        return rows

    def get_servidor(self, id):
        row = self.db(self.db.servidores.id == id).select().first()
        return row

    def insert_servidor(self, data):
        data['created_at'] = datetime.now()
        data['updated_at'] = datetime.now()
        try:
            id_servidor = self.db.servidores.insert(**data)
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
        return id_servidor

    def update_servidor(self, data, id):
        data['updated_at'] = datetime.now()
        try:
            self.db(self.db.servidores.id == id).update(**data)
            self.db.commit()
        except IntegrityError:
            self.db.rollback()

    def get_acceso_servidor(self, id):
        row = self.db(self.db.accesos_servidores.id_servidor == id).select(
            self.db.accesos_servidores.id_acceso
        ).first()
        acceso = self.db(self.db.accesos.id == row.id_acceso).select(
            self.db.accesos.username,
            self.db.accesos.password
        ).first()
        return acceso
