# coding=utf-8
from .modelo import DB
from psycopg2 import IntegrityError
from datetime import datetime


class Folders(object):

    def __init__(self):
        self.db = DB
        self.guarded = ['id', 'csrf_token']

    def clean_data(self, data):
        data = data.data
        for field in self.guarded:
            data.pop(field)
        return data

    def get_folders(self):
        rows = self.db(self.db.folders.id > 0).select(
            orderby=self.db.folders.name,
            cacheable=True
        )
        return rows

    def get_folder(self, id):
        row = self.db(self.db.folders.id == id).select().first()
        return row

    def insert_folder(self, data):
        data = self.clean_data(data)
        data['created_at'] = datetime.now()
        id_folder = None
        try:
            id_folder = self.db.folders.insert(**data)
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
        return id_folder

    def delete(self, id):
        result = 0
        try:
            self.db(self.db.folders.id == id).delete()
            self.db.commit()
            result = 1
        except IntegrityError:
            self.db.rollback()
        return result
