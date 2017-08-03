# -*- coding: utf-8 -*-

"""
gdown.module
~~~~~~~~~~~~~~~~~~~

Basic methods for modules.

"""

import requests
import random
import string

from .config import headers, proxies, max_retries


def acc_info_template():
    return {'email': None,
            'id': None,
            'status': None,
            'expire_date': None,
            'transfer': None,
            'points': None,
            'balance': None,
            'balance_currency': None}


def browser(proxy=False):
    r = requests.Session()
    r.mount('http://', requests.adapters.HTTPAdapter(max_retries=max_retries))
    r.mount('https://', requests.adapters.HTTPAdapter(max_retries=max_retries))
    r.headers = headers
    if proxy:
        r.proxies = proxies
    return r


def random_word(size=random.randint(1, 15), chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

# TODO: modules as classes
