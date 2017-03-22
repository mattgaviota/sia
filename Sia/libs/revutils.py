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

    def save_revision(self, comentario):
        """ Guarda un registro de actividad. """
        # TODO: Guardar revision según corresponda
