# coding=utf-8
from flask import Blueprint, render_template, url_for, flash
from flask import request, redirect, abort, session, current_app
from flask_login import login_user, login_required, logout_user
from ..forms import Login_form, User_form
from ..libs.utils import Utils
from ..modelos.users import Users
from logging import debug

auth = Blueprint(
    'auth',
    __name__,
    template_folder='templates'
)

USE_SESSION_FOR_NEXT = False

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = Login_form()
    if form.validate_on_submit():
        user = Users().get_user(username=form.username.data)
        if user:
            if user.is_correct_password(form.password.data):
                login_user(user)
                session['username'] = 'mattgaviota'
                flash(
                    'Ha ingresado correctamente.',
                    'success'
                )
                next = session.get('next')
                current_app.logger.debug(next)
                if not Utils().is_safe_url(next):
                    return abort(400)
                return redirect(next or url_for('home.index'))
            else:
                flash('usuario y/o password incorrecto', 'error')
                return redirect(url_for('home.index'))
        else:
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
    logout_user()
    flash('Has salido correctamente.', 'success')
    return redirect(url_for('home.index'))
