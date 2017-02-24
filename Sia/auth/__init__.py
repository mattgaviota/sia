# coding=utf-8
from flask import Blueprint, render_template, request

auth = Blueprint(
    'auth',
    __name__,
    template_folder='templates'
)


@auth.route('/login')
def login():
    """Login form"""
    return render_template('login.html.jinja')


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
