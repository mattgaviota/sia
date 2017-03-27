# coding=utf-8
from .modelo import DB
from psycopg2 import IntegrityError
from datetime import datetime


class Revisions(object):

    def __init__(self):
        self.db = DB

    def get_revisions(self):
        rows = self.db(self.db.revisions.id > 0).select(
            orderby=~self.db.revisions.created_at,
            cacheable=True
        )
        return rows

    def get_revision(self, id):
        row = self.db(self.db.revisions.id == id).select().first()
        return row

    def get_revisions_by_user(self, user):
        rows = self.db(self.db.revisions.id_user == user.user_id).select(
            orderby=~self.db.revisions.created_at
        )
        return rows

    def insert_revision(self, data):
        data['created_at'] = datetime.now()
        try:
            self.db.revisions.insert(**data)
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
