# coding=utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, HiddenField, SelectField
from wtforms.validators import DataRequired


class Servidor_form(FlaskForm):
    """docstring for Servidor_form."""
    id = HiddenField('id')
    name = StringField(
        'Nombre del Establecimiento',
        validators=[DataRequired(message="Este campo es requerido")]
    )
    ip = StringField(
        'Dirección del servidor de la base origen',
        validators=[DataRequired(message="Este campo es requerido")]
    )
    port = StringField(
        'Puerto del servidor de la base origen',
        validators=[DataRequired(message="Este campo es requerido")]
    )
    dbname = StringField('Nombre de la base origen')
    db_dest = StringField('Nombre de la base destino')
    id_servidor_destino = SelectField(
        'Servidor Destino',
        coerce=int,
        description='Elija un servidor'
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
        validators=[DataRequired()]
    )
    username = StringField(
        'Usuario de acceso',
        validators=[DataRequired()]
    )
    password = StringField(
        'Contraseña de acceso',
        validators=[DataRequired()]
    )
