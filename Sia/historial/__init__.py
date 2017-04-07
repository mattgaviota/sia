# coding=utf-8
from flask import Blueprint, render_template, request
from flask_login import login_required
from ..libs import is_admin
from ..libs.revutils import Revisioner, Pagination


historial = Blueprint(
    'historial',
    __name__,
    template_folder='templates'
)

PER_PAGE = 10


@historial.route('/', defaults={'page': 1})
@historial.route('/page/<int:page>')
@login_required
@is_admin
def index(page):
    """index all revisions"""
    count = Revisioner().count_all_revisions()
    revisiones = Revisioner().get_revisions_for_page(page, PER_PAGE)
    if not revisiones and page != 1:
        abort(404)
    pagination = Pagination(page, PER_PAGE, count)
    return render_template(
        'historial/index.html.jinja',
        revisiones=revisiones,
        pagination=pagination
    )

@historial.route('/user/<user_id>/', defaults={'page': 1})
@historial.route('/user/<user_id>/<int:page>')
@login_required
@is_admin
def user(user_id, page):
    """user revisions"""
    count = Revisioner().count_all_revisions_by_user(user_id)
    revisiones = Revisioner().get_revisions_for_page_by_user(
        user_id,
        page,
        PER_PAGE
    )
    if not revisiones and page != 1:
        abort(404)
    pagination = Pagination(page, PER_PAGE, count)
    usuario = revisiones[0]['usuario']
    return render_template(
        'historial/user.html.jinja',
        revisiones=revisiones,
        pagination=pagination,
        usuario=usuario
    )
