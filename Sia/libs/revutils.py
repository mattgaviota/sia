# coding=utf-8

from ..modelos.revisions import Revisions
from ..modelos.types import Types


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

    def get_revisions_by_user(self, user):
        """ Retorna la actividad de un usuario. """
        # TODO: formatear revisiones
        return Revisions().get_revisions_by_user(user)

    def get_all_revisions(self):
        """ Retorna todas las actividades. """
        # TODO: formatear revisiones
        return Revisions().get_revisions()
