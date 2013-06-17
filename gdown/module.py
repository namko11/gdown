# -*- coding: utf-8 -*-

"""
gdown.module
~~~~~~~~~~~~~~~~~~~

Basic methods for modules.

"""

import requests
import random
import string

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


def random_word():
    lenght = random.randint(1, 15)
    return ''.join(random.choice(string.lowercase) for i in range(lenght))

# TODO: modules as classes
