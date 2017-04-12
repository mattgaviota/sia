# coding=utf-8
from flask import Blueprint, render_template, request
from flask_login import login_required
from ..libs.revutils import Pagination
from ..libs.conutils import Viewer


consolidacion = Blueprint(
    'consolidacion',
    __name__,
    template_folder='templates'
)

PER_PAGE = 20

@consolidacion.route('/')
@login_required
def index():
    return render_template('consolidacion/index.html.jinja')

@consolidacion.route('/estadisticas', defaults={'page': 1})
@consolidacion.route('/estadisticas/page/<int:page>')
@login_required
def estadisticas(page):
    """Muestra las estadisticas"""
    count = Viewer().count_estadisticas()
    estadisticas = Viewer().get_estadisticas_per_page(page, PER_PAGE)
    if not estadisticas and page != 1:
        abort(404)
    pagination = Pagination(page, PER_PAGE, count)
    return render_template(
        'consolidacion/estadisticas.html.jinja',
        estadisticas=estadisticas,
        pagination=pagination
    )

@consolidacion.route('/backups', defaults={'page': 1})
@consolidacion.route('/backups/<int:page>')
@login_required
def backups(page):
    """user revisions"""
    count = Viewer().count_backups()
    backups = Viewer().get_backups_per_page(page, PER_PAGE)
    if not backups and page != 1:
        abort(404)
    pagination = Pagination(page, PER_PAGE, count)
    return render_template(
        'consolidacion/backups.html.jinja',
        backups=backups,
        pagination=pagination
    )
