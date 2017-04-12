# coding=utf-8

from ..modelos.modelo_consolidado import Consolidacion


class Viewer(object):

    def __init__(self):
        super(Viewer, self).__init__()

    def count_estadisticas(self):
        return Consolidacion().count_estadisticas()

    def count_backups(self):
        return Consolidacion().count_backups()

    def get_estadisticas_per_page(self, page, per_page):
        """ Retorna las estadísticas por pagina. """
        estadisticas = Consolidacion().get_estadisticas_for_page(
            page,
            per_page
        )
        return estadisticas

    def get_backups_per_page(self, page, per_page):
        """ Retorna las backups por pagina. """
        backups = Consolidacion().get_backups_for_page(
            page,
            per_page
        )
        return backups
