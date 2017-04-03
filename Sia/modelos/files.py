# coding=utf-8
from .modelo import DB
from psycopg2 import IntegrityError
from datetime import datetime


class Files(object):

    def __init__(self):
        self.db = DB

    def get_files(self):
        rows = self.db(self.db.files.id > 0).select(
            orderby=self.db.files.name,
            cacheable=True
        )
        return rows

    def get_files_by_folder(self, id_folder):
        rows = self.db(self.db.files.id_folder == id_folder).select(
            orderby=self.db.files.name,
            cacheable=True
        )
        return rows

    def get_file(self, id):
        row = self.db(self.db.files.id == id).select().first()
        return row

    def insert_file(self, data):
        data['created_at'] = datetime.now()
        id_file = None
        try:
            id_file = self.db.files.insert(**data)
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
        return id_file

    def delete(self, id):
        result = 0
        try:
            self.db(self.db.files.id == id).delete()
            self.db.commit()
            result = 1
        except IntegrityError:
            self.db.rollback()
        return result
