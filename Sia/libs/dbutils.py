# coding=utf-8

from .utils import Utils
from ..modelos.servidores import Servidores
from ..modelos.accesos import Accesos
import os
import subprocess


class DButils(object):
    """docstring for DButils."""
    def __init__(self, **kwargs):
        super(DButils, self).__init__()
        self.host = kwargs['host']
        self.port = kwargs['port']
        self.dbname = kwargs['dbname']
        self.acceso = Accesos().get_acceso(kwargs['id_acceso'])
        self.utils = Utils()
        self.dbschemas = 'public'

    def set_pass(self):
        os.putenv('PGPASSWORD', self.acceso.password)

    def exists_host(self):
        self.set_pass()
        try:
            result = subprocess.check_output(
                [
                    'psql',
                    '-h', self.host,
                    '-p', self.port,
                    '-U', self.acceso.username,
                    '-d', self.dbname,
                    '-c', '\q'
                ]
            )
            if not result:
                return 1
        except subprocess.CalledProcessError:
            pass
        return 0


    def make_dump(self, new_dump):
        """
            Realiza un dump con el nombre new_dump con los datos de
            DBNAME, DBHOST, DBUSER y DBPASS
        """
        dump = new_dump.lower().replace(' ', '_') + '_{}.sql'.format(self.dbname)
        self.set_pass()
        result = subprocess.call(
            [
                'pg_dump',
                '-h', self.host,
                '-p', self.port,
                '-U', self.acceso.username,
                '-Fc',
                '-d', self.dbname,
                '-n', self.dbschemas,
                '-f', dump
            ],
            stdout=subprocess.PIPE
        )
        self.utils.compress_file(dump)
        if not result:
            return dump
        return ''


    def make_backup(self, nombre):
        result = ''
        if self.exists_host():
            result = self.make_dump(nombre)
        return result


    def exec_command(self, command):
        self.set_pass()
        return subprocess.call(
            [
                'psql',
                '-h', self.host,
                '-p', self.port,
                '-U', self.acceso.username,
                '-c', command
            ],
            stdout=subprocess.PIPE
        )


    def create_db(self):
        command = 'CREATE DATABASE {};'.format(self.dbname)
        self.exec_command(command)


    def drop_db(self, fname):
        terminate = "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE "
        terminate += "pid <> pg_backend_pid() AND datname = '{}';".format(self.dbname)
        self.exec_command(terminate)
        command = 'DROP DATABASE {};'.format(self.dbname)
        self.exec_command(command)
        subprocess.call(['rm', fname], stdout=subprocess.PIPE)

    def restore_db(self, fname, clean_db=False):
        self.set_pass()
        clean_db_opt = '-c'
        if clean_db:
            clean_db_opt = '-v'
        result = subprocess.call(
            [
                'pg_restore',
                '-h', self.host,
                '-p', self.port,
                '-U', self.acceso.username,
                '-n', self.dbschemas,
                '-d', self.dbname,
                clean_db_opt,
                fname
            ],
            stdout=subprocess.PIPE
        )
        subprocess.call(['rm', fname], stdout=subprocess.PIPE)
        return result


class Handler(object):
    """docstring for Handler."""
    def __init__(self, servidor_origen, servidor_destino, form):
        super(Handler, self).__init__()
        self.origen = DButils(
            host=servidor_origen.ip,
            port=servidor_origen.port,
            dbname=servidor_origen.dbname,
            id_acceso=servidor_origen.id_acceso
        )
        self.destino = DButils(
            host=servidor_destino.ip,
            port=servidor_destino.port,
            dbname=form.db_dest.data,
            id_acceso=servidor_destino.id_acceso
        )
        self.hospital = servidor_origen.name
        try:
            self.clean_db = form.clean_db.data
        except AttributeError:
            self.clean_db = False

    def validar_script(self):
        """ Valida los pasos a seguir en el script. """
        messages = []
        if not self.origen.exists_host():
            messages.append("""
                No se puede realizar un backup de la base <strong>{}</strong>
                del servidor <strong>{}</strong> en el puerto <strong>{}</strong>.
            """.format(self.origen.dbname, self.origen.host, self.origen.port))
            return messages
        messages.append("""
            Se realizará un backup de la base <strong>{}</strong>
            del servidor <strong>{}</strong> en el puerto <strong>{}</strong>.
        """.format(self.origen.dbname, self.origen.host, self.origen.port))
        message = """
            Se realizará un backup de la base <strong>{}</strong>
            del servidor <strong>{}</strong> en el puerto <strong>{}</strong>.
        """.format(self.destino.dbname, self.destino.host, self.destino.port)
        if not self.destino.exists_host():
            message = """
                Se creará la base <strong>{}</strong> del servidor
                <strong>{}</strong> en el puerto <strong>{}</strong>.
            """.format(self.destino.dbname, self.destino.host, self.destino.port)
        messages.append(message)
        clean_db_msg = '<strong>sólo los datos</strong> de'
        if self.clean_db:
            clean_db_msg = ''
        message = """
            Se remplazará {} la base <strong>{}</strong> del servidor
            <strong>{}</strong> en el puerto <strong>{}</strong>.
            con el backup de la base <strong>{}</strong>
            del servidor <strong>{}</strong> en el puerto <strong>{}</strong>.
        """.format(
            clean_db_msg,
            self.destino.dbname, self.destino.host, self.destino.port,
            self.origen.dbname, self.origen.host, self.origen.port
        )
        messages.append(message)
        return messages

    def restaurar_db(self):
        messages = []
        bkp_origen = self.origen.make_backup(self.hospital)
        if bkp_origen:
            bkp_dest = self.destino.make_backup(self.hospital)
            if bkp_dest:
                message = """
                    Se realizó un backup de la base <strong>{}</strong>
                    en el servidor <strong>{}</strong> en el puerto <strong>{}</strong>.
                """.format(self.destino.dbname, self.destino.host, self.destino.port)
                messages.append(message)
                res_create = 1
                if self.clean_db:
                    self.destino.drop_db(bkp_dest)
                    res_create = self.destino.create_db()
            else:
                res_create = self.destino.create_db()
            if not res_create:
                message = """
                    Se creó la base <strong>{}</strong>
                    en el servidor <strong>{}</strong> en el puerto <strong>{}</strong>.
                """.format(self.destino.dbname, self.destino.host, self.destino.port)
                messages.append(message)
            res_restore = self.destino.restore_db(bkp_origen, self.clean_db)
            print(res_restore)
            message = """
                Se restauró la base <strong>{}</strong> con el backup de la base
                <strong>{}</strong> del servidor <strong>{}</strong>.
                En el servidor <strong>{}</strong> en el puerto <strong>{}</strong>.
            """.format(
                self.destino.dbname, self.origen.dbname, self.origen.host,
                self.destino.host, self.destino.port
            )
            messages.append(message)
        else:
            messages.append("""
                No se pudo realizar un backup de la base <strong>{}</strong>
                en el servidor <strong>{}</strong> en el puerto <strong>{}</strong>.
            """.format(self.origen.dbname, self.origen.host, self.origen.port))
            return messages
        return messages
