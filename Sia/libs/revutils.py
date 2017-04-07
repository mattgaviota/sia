# coding=utf-8

from datetime import datetime
from math import ceil
from ..modelos.comandos import Comandos
from ..modelos.revisions import Revisions
from ..modelos.types import Types
from ..modelos.users import Users


class Revisioner(object):
    """docstring for Handler."""
    def __init__(self, user=None, comando=None, type_prefijo=None):
        super(Revisioner, self).__init__()
        self.comando = comando
        self.user = user
        self.type = Types().get_type_by_prefix(type_prefijo)

    def save_revision(self, comentario=''):
        """ Guarda un registro de actividad. """
        data = {}
        if self.comando:
            data['id_comando'] = self.comando.id
        if self.type:
            data['id_type'] = self.type.id
        data['id_user'] = self.user.user_id
        data['comentario'] = comentario
        Revisions().insert_revision(data)

    def get_revisions_by_user(self, user_id):
        """ Retorna la actividad de un usuario. """
        revisiones = Revisions().get_revisions_by_user(
            Users().get_user(user_id=user_id)
        )
        if not revisiones:
            return []
        historial = []
        usuario = Users().get_user(user_id=user_id).get_name()
        for revision in revisiones:
            fecha = datetime.strftime(revision.created_at, '%d/%m/%Y %H:%M')
            mensaje = ''
            if revision.id_comando:
                comando = Comandos().get_comando(revision.id_comando).title
                mensaje = 'Ejecutó {} '.format(comando)
            mensaje += revision.comentario
            historial.append({
                'id': revision.id,
                'user_id': revision.id_user,
                'usuario': usuario,
                'mensaje': mensaje,
                'fecha': fecha
            })
        return historial

    def get_revisions_for_page_by_user(self, user_id, page, per_page):
        """ Retorna la actividad de un usuario por página. """
        revisiones = Revisions().get_revisions_for_page_by_user(
            Users().get_user(user_id=user_id),
            page,
            per_page
        )
        if not revisiones:
            return []
        historial = []
        usuario = Users().get_user(user_id=user_id).get_name()
        for revision in revisiones:
            fecha = datetime.strftime(revision.created_at, '%d/%m/%Y %H:%M')
            mensaje = ''
            if revision.id_comando:
                comando = Comandos().get_comando(revision.id_comando).title
                mensaje = 'Ejecutó {} '.format(comando)
            mensaje += revision.comentario
            historial.append({
                'id': revision.id,
                'user_id': revision.id_user,
                'usuario': usuario,
                'mensaje': mensaje,
                'fecha': fecha
            })
        return historial

    def get_all_revisions(self):
        """ Retorna todas las actividades. """
        revisiones = Revisions().get_revisions()
        if not revisiones:
            return []
        historial = []
        for revision in revisiones:
            fecha = datetime.strftime(revision.created_at, '%d/%m/%Y %H:%M')
            usuario = Users().get_user(user_id=revision.id_user).get_name()
            mensaje = ''
            if revision.id_comando:
                comando = Comandos().get_comando(revision.id_comando).title
                mensaje = 'Ejecutó {} '.format(comando)
            mensaje += revision.comentario
            historial.append({
                'id': revision.id,
                'user_id': revision.id_user,
                'usuario': usuario,
                'mensaje': mensaje,
                'fecha': fecha
            })
        return historial

    def count_all_revisions(self):
        return Revisions().count_revisions()

    def count_all_revisions_by_user(self, user_id):
        return Revisions().count_revisions_by_user(
            Users().get_user(user_id=user_id)
        )

    def get_revisions_for_page(self, page, per_page):
        """ Retorna las actividades por pagina. """
        revisiones = Revisions().get_revisions_for_page(page, per_page)
        if not revisiones:
            return []
        historial = []
        for revision in revisiones:
            fecha = datetime.strftime(revision.created_at, '%d/%m/%Y %H:%M')
            usuario = Users().get_user(user_id=revision.id_user).get_name()
            mensaje = ''
            if revision.id_comando:
                comando = Comandos().get_comando(revision.id_comando).title
                mensaje = 'Ejecutó {} '.format(comando)
            mensaje += revision.comentario
            historial.append({
                'id': revision.id,
                'user_id': revision.id_user,
                'usuario': usuario,
                'mensaje': mensaje,
                'fecha': fecha
            })
        return historial


class Pagination(object):

    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in range(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and \
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num
