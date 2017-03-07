# coding=utf-8
from .modelo import DB
from psycopg2 import IntegrityError
from datetime import datetime
from .. import bcrypt


class Users(object):
    # TODO: Completar con los metodos requeridos por flask_login
    # TODO: usar bcrypt para almacenar el password
    # https://exploreflask.com/en/latest/users.html
    def __init__(self):
        self.db = DB
        self.guarded = ['id', 'csrf_token']

    def clean_data(self, data):
        data = data.data
        for field in self.guarded:
            data.pop(field)
        return data

    def get_user(self, id):
        row = self.db(self.db.users.id == id).select().first()
        return row

    def insert_user(self, data):
        data = self.clean_data(data)
        data['created_at'] = datetime.now()
        data['updated_at'] = datetime.now()
        id_user = None
        try:
            id_user = self.db.accesos.insert(**data)
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
        return id_user

    def update_user(self, data):
        id_user = data.id.data
        data = self.clean_data(data)
        data['updated_at'] = datetime.now()
        result = 0
        try:
            self.db(self.db.users.id == id_user).update(**data)
            self.db.commit()
            result = 1
        except IntegrityError:
            self.db.rollback()
        return result

    def delete(self, id):
        result = 0
        try:
            self.db(self.db.users.id == id).delete()
            self.db.commit()
            result = 1
        except IntegrityError:
            self.db.rollback()
        return result
