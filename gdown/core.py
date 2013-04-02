# -*- coding: utf-8 -*-

"""
gdown.core
~~~~~~~~~~~~~~~~~~~

This module implements the gdown's basic methods.

"""

import requests

from .config import headers


def browser():
    r = requests.Session()
    r.headers = headers
    return r
