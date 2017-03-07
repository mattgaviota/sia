# coding=utf-8
import os
import tarfile
from urllib.parse import urlparse, urljoin
from flask import request, url_for


class Utils(object):
    """docstring for Utils."""
    def __init__(self):
        super(Utils, self).__init__()

    def compress_file(self, namefile, suffix='sql'):
        """ Comprime un archivo sql en un tar.gz con el mismo nombre que tenia. """
        tarfile_name = namefile.replace(suffix, 'tar.gz')
        tar_file = tarfile.open(tarfile_name, 'w:gz')
        tar_file.add(namefile, arcname=os.path.basename(namefile))
        tar_file.close()
        return tarfile_name

    def is_safe_url(target):
        ref_url = urlparse(request.host_url)
        test_url = urlparse(urljoin(request.host_url, target))
        return test_url.scheme in ('http', 'https') and \
               ref_url.netloc == test_url.netloc
