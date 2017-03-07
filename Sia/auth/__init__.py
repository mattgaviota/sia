# coding=utf-8
from flask import Blueprint, render_template, request, redirect, abort
from flask_login import login_user
from ..forms import Login_form
from ..libs.utils import Utils
from ..modelos.users import Users

auth = Blueprint(
    'auth',
    __name__,
    template_folder='templates'
)


def load_user(user_id):
    return Users().get_user(user_id)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = Login_form()
    if form.validate_on_submit():
        # TODO: Falta validar usuario https://exploreflask.com/en/latest/users.html
        login_user(user)

        flash('Logged in successfully.')

        next = request.args.get('next')

        if not Utils().is_safe_url(next):
            return abort(400)

        return redirect(next or url_for('admin.index'))
    return render_template('auth/login.html.jinja', form=form)


@auth.route('/register')
def register():
    """Formulario de registro"""
    return render_template('register.html.jinja')


@auth.route('/register', methods=['POST'])
def registration():
    """ Realiza el registro de un nuevo usuario. """
    new_user = request.form
    return render_template('success.html.jinja')


@auth.route('/logon', methods=['POST'])
def logon():
    """ Método que realiza el login. """
    user_login = request.form
    return redirect(url_for('home.index'))


@auth.route('/logout')
def logout():
    """ Método que realiza el logout. """
    return redirect(url_for('auth.login'))
