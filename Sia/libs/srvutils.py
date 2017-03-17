# coding=utf-8

from .utils import Utils
from ..modelos.accesos import Accesos
import os
import subprocess

PATH_SSH_KEY = '/var/www/.ssh/id_rsa'


class Runner(object):
    """docstring for Handler."""
    def __init__(self, comando, servidor):
        super(Runner, self).__init__()
        self.comando = comando
        self.servidor = servidor
        self.acceso = Accesos().get_acceso(self.servidor.id_acceso)

    def run(self):
        """ Ejecuta el comando. """
        try:
            output = subprocess.check_output(
                [
                    'sshpass',
                    '-p', self.acceso.password,
                    'ssh',
                    '-p', self.servidor.port,
                    self.acceso.username + '@' + self.servidor.host,
                    self.comando.name,
                    self.comando.options
                ]
            )
            output = str(output, 'utf8')
        except subprocess.CalledProcessError:
            output = 'Hubo un error al lanzar el comando.'
        cmd_run = 'ssh -p {} {}@{} {} {}'.format(
            self.servidor.port,
            self.acceso.username,
            self.servidor.host,
            self.comando.name,
            self.comando.options
        )
        return {'output': output, 'cmd_run': cmd_run}
