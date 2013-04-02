# -*- coding: utf-8 -*-

"""
gdown.core
~~~~~~~~~~~~~~~~~~~

This module implements the gdown's basic methods.

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
