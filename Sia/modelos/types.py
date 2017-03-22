# coding=utf-8
from .modelo import DB
from psycopg2 import IntegrityError
from datetime import datetime


class Types(object):

    def __init__(self):
        self.db = DB

    def get_types(self):
        rows = self.db(self.db.types.id > 0).select(
            orderby=self.db.types.created_at,
            cacheable=True
        )
        return rows

    def get_type(self, id):
        row = self.db(self.db.types.id == id).select().first()
        return row

    def get_types_by_prefix(self, prefix):
        row = self.db(self.db.types.prefijo == prefix).select().first()
        return row

    def insert_type(self, data):
        data['created_at'] = datetime.now()
        data['updated_at'] = datetime.now()
        try:
            self.db.types.insert(**data)
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
