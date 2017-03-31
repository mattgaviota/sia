# coding=utf-8
from flask import Blueprint, render_template, url_for, flash
from flask import request, redirect
from flask_login import login_user, login_required, logout_user, current_user
from ..forms import Login_form, User_form, Password_form
from ..libs.utils import Utils
from ..libs.revutils import Revisioner
from ..libs import is_admin
from ..modelos.users import Users

auth = Blueprint(
    'auth',
    __name__,
    template_folder='templates'
)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    next = request.args.get('next')
    form = Login_form()
    if form.validate_on_submit():
        user = Users().get_user(username=form.username.data)
        if user:
            if user.is_correct_password(form.password.data):
                login_user(user)
                Revisioner(user=user).save_revision('Ingresó al sistema')
                flash(
                    'Ha ingresado correctamente.',
                    'success'
                )
                next = request.form['next']
                if not Utils().is_safe_url(next):
                    return redirect(url_for('home.index'))
                return redirect(next)
            flash('usuario y/o password incorrecto', 'error')
        else:
            flash('usuario y/o password incorrecto', 'error')
    return render_template('auth/login.html.jinja', form=form, next=next)


@auth.route('/register', methods=['GET', 'POST'])
@login_required
@is_admin
def register():
    """ Realiza el registro de un nuevo usuario. """
    form = User_form()
    if form.validate_on_submit():
        Users().insert_user(form)
        Revisioner(user=current_user).save_revision(
            'Creó el usuario {} {}'.format(
                form.data['name'],
                form.data['last_name']
            )
        )
        flash('Registrado correctamente.', 'success')
        return redirect(url_for('admin.index'))
    return render_template('auth/register.html.jinja', form=form)


@auth.route('/logout')
@login_required
def logout():
    """ Método que realiza el logout. """
    Revisioner(user=current_user).save_revision('Salió del sistema')
    logout_user()
    flash('Has salido correctamente.', 'success')
    return redirect(url_for('home.index'))


@auth.route('/change_pass', methods=['GET', 'POST'])
@login_required
def change_pass():
    """ Método que realiza el cambio de password. """
    form = Password_form()
    if form.validate_on_submit():
        if current_user.update_password(form):
            flash('Registrado correctamente.', 'success')
            Revisioner(user=current_user).save_revision('Cambió su contraseña')
            logout_user()
            return redirect(url_for('home.index'))
        flash('La contraseña actual no corresponde al usuario.', 'error')
    return render_template('auth/change_pass.html.jinja', form=form)
