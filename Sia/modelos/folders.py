# coding=utf-8
from .modelo import DB
from psycopg2 import IntegrityError
from datetime import datetime


class Folders(object):

    def __init__(self):
        self.db = DB

    def get_folders(self):
        rows = self.db(self.db.folders.id > 0).select(
            orderby=~self.db.folders.created_at,
            cacheable=True
        )
        return rows

    def get_last_folder(self, folder_id=None):
        if folder_id:
            rows = self.db(self.db.folders.id != folder_id).select(
                orderby=~self.db.folders.created_at,
                cacheable=True
            )
        else:
            rows = self.get_folders()
        return rows[0]

    def get_folder(self, id):
        row = self.db(self.db.folders.id == id).select().first()
        return row

    def get_folder_by_name(self, name):
        row = self.db(self.db.folders.name == name).select().first()
        return row

    def insert_folder(self, data):
        data['created_at'] = datetime.now()
        id_folder = None
        try:
            self.update_folders()
            id_folder = self.db.folders.insert(**data)
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
        return id_folder

    def update_folder(self, folder_id):
        self.db(self.db.folders.id == folder_id).update(**{'latest': 't'})
        self.db.commit()

    def update_folders(self):
        self.db(self.db.folders.id > 0).update(**{'latest': 'f'})
        self.db.commit()

    def delete(self, id):
        result = 0
        try:
            self.db(self.db.folders.id == id).delete()
            self.db.commit()
            result = 1
        except IntegrityError:
            self.db.rollback()
        return result
