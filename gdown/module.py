# -*- coding: utf-8 -*-

"""
gdown.module
~~~~~~~~~~~~~~~~~~~

Basic methods for modules.

"""

import requests
import random
import string

from .config import headers, proxies


def acc_info_template():
    return {'email': None,
            'id': None,
            'status': None,
            'expire_date': None,
            'transfer': None,
            'points': None}


def browser(proxy=False):
    r = requests.Session()
    r.headers = headers
    if proxy:
        r.proxies = proxies
    return r


def random_word(size=random.randint(1, 15), chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

# TODO: modules as classes
