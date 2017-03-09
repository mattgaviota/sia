# coding=utf-8
from .modelo import DB
from psycopg2 import IntegrityError
from datetime import datetime
from flask import current_app
from flask_bcrypt import Bcrypt

class Users(object):
    # TODO: Completar con los metodos requeridos por flask_login
    def __init__(self):
        self.db = DB
        self.guarded = ['id', 'csrf_token', 'password_rep']
        self.bcrypt = Bcrypt(current_app)
        self.active = False
        self.authenticated = False

    def is_correct_password(self, plaintext):
        return self.bcrypt.check_password_hash(self.password, plaintext)

    @property
    def is_active(self):
        return self._is_active

    @property
    def is_authenticated(self):
        return self._is_authenticated

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.user_id)

    def set_authenticated(self):
        self._is_authenticated = True

    def clean_data(self, data):
        data = data.data
        for field in self.guarded:
            data.pop(field)
        return data

    def get_name(self):
        return self.name

    def get_user(self, user_id=None, username=None):
        row = None
        if user_id and user_id != 'None':
            row = self.db(self.db.users.id == int(user_id)).select().first()
        if username:
            row = self.db(self.db.users.login == username).select().first()
        if row:
            self.user_id = user_id
            self.username = row.login
            self.name = row.name + ' ' + row.last_name
            self.password = row.password
            self.is_admin = row.is_admin
            self._is_active = True
            return self
        else:
            return None

    def insert_user(self, data):
        data = self.clean_data(data)
        data['created_at'] = datetime.now()
        data['updated_at'] = datetime.now()
        data['password'] = self.bcrypt.generate_password_hash(data['password'])
        id_user = None
        try:
            id_user = self.db.users.insert(**data)
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
