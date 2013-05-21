# -*- coding: utf-8 -*-

"""
gdown.module
~~~~~~~~~~~~~~~~~~~

Basic methods for modules.

"""

import requests

from .config import headers


def acc_info_template():
    return {'email': None,
            'id': None,
            'status': None,
            'expire_date': None,
            'transfer': None,
            'points': None}


def browser():
    r = requests.Session()
    r.headers = headers
    return r

# TODO: modules as classes
