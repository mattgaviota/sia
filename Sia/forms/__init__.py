# coding=utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, HiddenField
from wtforms import SelectField, PasswordField
from wtforms.validators import DataRequired, EqualTo


class Establecimiento_form(FlaskForm):
    """docstring for Establecimiento_form."""
    id = HiddenField('id')
    name = StringField(
        'Nombre del Establecimiento',
        validators=[DataRequired(message="Este campo es requerido")]
    )
    ip = StringField(
        'Dirección del establecimiento de la base origen',
        validators=[DataRequired(message="Este campo es requerido")]
    )
    port = StringField(
        'Puerto del establecimiento de la base origen',
        validators=[DataRequired(message="Este campo es requerido")]
    )
    dbname = StringField('Nombre de la base origen')
    db_dest = StringField('Nombre de la base destino')
    id_establecimiento_destino = SelectField(
        'Servidor Destino',
        coerce=int,
        description='Elija un establecimiento'
    )
    id_acceso = SelectField(
        'Datos de Acceso',
        coerce=int,
        description='Elija un acceso'
    )
    clean_db = BooleanField('Recrear la DB destino')


class Acceso_form(FlaskForm):
    id = HiddenField('id')
    name = StringField(
        'Nombre del acceso',
        validators=[DataRequired(message="Este campo es requerido")]
    )
    username = StringField(
        'Usuario de acceso',
        validators=[DataRequired(message="Este campo es requerido")]
    )
    password = StringField(
        'Contraseña de acceso',
        validators=[DataRequired(message="Este campo es requerido")]
    )


class Login_form(FlaskForm):
    username = StringField(
        'Usuario',
        validators=[DataRequired(message="Este campo es requerido")]
    )
    password = PasswordField(
        'Contraseña',
        validators=[DataRequired(message="Este campo es requerido")]
    )


class User_form(FlaskForm):
    id = HiddenField('id')
    name = StringField(
        'Nombre',
        validators=[DataRequired(message="Este campo es requerido")]
    )
    last_name = StringField(
        'Apellido',
        validators=[DataRequired(message="Este campo es requerido")]
    )
    login = StringField(
        'Nombre de Usuario',
        validators=[DataRequired(message="Este campo es requerido")]
    )
    password = PasswordField(
        'Contraseña',
        validators=[
            DataRequired(message="Este campo es requerido"),
            EqualTo('password_rep', message="Las contraseñas deben coincidir")
        ]
    )
    password_rep = PasswordField(
        'Vuelva a escribir la Contraseña',
        validators=[DataRequired(message="Este campo es requerido")]
    )
    is_admin = BooleanField('Es administrador')


class Password_form(FlaskForm):
    password_old = PasswordField(
        'Contraseña actual',
        validators=[DataRequired(message="Este campo es requerido")]
    )
    password = PasswordField(
        'Contraseña nueva',
        validators=[
            DataRequired(message="Este campo es requerido"),
            EqualTo('password_rep', message="Las contraseñas deben coincidir")
        ]
    )
    password_rep = PasswordField(
        'Repetir Contraseña',
        validators=[DataRequired(message="Este campo es requerido")]
    )


class Servidor_form(FlaskForm):
    """docstring for Servidor_form."""
    id = HiddenField('id')
    name = StringField(
        'Nombre del Servidor',
        validators=[DataRequired(message="Este campo es requerido")]
    )
    host = StringField(
        'Dirección remota del servidor',
        validators=[DataRequired(message="Este campo es requerido")]
    )
    port = StringField(
        'Puerto para acceder al servidor',
        validators=[DataRequired(message="Este campo es requerido")]
    )
    id_acceso = SelectField(
        'Datos de Acceso',
        coerce=int,
        description='Elija un acceso'
    )
