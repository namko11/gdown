# -*- coding: utf-8 -*-

"""
gdown.module
~~~~~~~~~~~~~~~~~~~

Basic methods for modules.

"""

import requests

from .config import headers


acc_info = {'email': None,
            'id': None,
            'status': None,
            'expire_date': None}


def browser():
    r = requests.Session()
    r.headers = headers
    return r
