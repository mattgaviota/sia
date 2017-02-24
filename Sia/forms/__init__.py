# coding=utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired


class Servidor_form(FlaskForm):
    """docstring for Servidor_form."""
    ip = StringField(
        'Dirección del servidor de la base origen',
        validators=[DataRequired()]
    )
    port = StringField(
        'Puerto del servidor de la base origen',
        validators=[DataRequired()]
    )
    dbname = StringField(
        'Nombre de la base origen',
        validators=[DataRequired()]
    )
    ip_dest = StringField(
        'Dirección del servidor destino',
        validators=[DataRequired()]
    )
    port_dest = StringField(
        'Puerto del servidor de la base origen',
        validators=[DataRequired()]
    )
    db_dest = StringField(
        'Nombre de la base destino',
        validators=[DataRequired()]
    )
    clean_db = BooleanField('Recrear la DB destino')


class Acceso_form(FlaskForm):
    username = StringField(
        'Usuario de acceso',
        validators=[DataRequired()]
    )
    password = StringField(
        'Contraseña de acceso',
        validators=[DataRequired()]
    )
