# coding=utf-8
from flask import Blueprint, render_template, url_for, flash
from flask import request, redirect, abort, current_app
from flask_login import login_user, login_required
from ..forms import Login_form, User_form
from ..libs.utils import Utils
from ..modelos.users import Users

auth = Blueprint(
    'auth',
    __name__,
    template_folder='templates'
)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = Login_form()
    if form.validate_on_submit():
        user = Users().get_user(username=form.username.data)
        if user:
            if user.is_correct_password(form.password.data):
                user.set_authenticated()
                login_user(user)
                flash(
                    'Ha ingresado correctamente. %s'.format(user.get_name()),
                    'success'
                )
                return redirect(url_for('admin.index'))
        flash('usuario y/o password incorrecto', 'error')
        return redirect(url_for('home.index'))
    return render_template('auth/login.html.jinja', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """ Realiza el registro de un nuevo usuario. """
    form = User_form()
    if form.validate_on_submit():
        Users().insert_user(form)
        flash('Registrado correctamente.', 'success')
        return redirect(url_for('home.index'))
    return render_template('auth/register.html.jinja', form=form)


@auth.route('/logout')
@login_required
def logout():
    """ Método que realiza el logout. """
    return redirect(url_for('auth.login'))
