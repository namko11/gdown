# -*- coding: utf-8 -*-

"""
gdown.modules.lunaticfiles
~~~~~~~~~~~~~~~~~~~

This module contains handlers for lunaticfiles.

"""

import re
from dateutil import parser
# from datetime import datetime

from ..module import browser, acc_info_template
from ..exceptions import ModuleError


def accInfo(username, passwd, proxy=False):
    """Returns account info."""
    acc_info = acc_info_template()
    r = browser(proxy)
    data = {'op': 'login',
            'login': username,
            'password': passwd,
            'redirect': 'http://lunaticfiles.com/?op=my_account'}
    rc = r.post('http://lunaticfiles.com', data=data).text
    open('gdown.log', 'w').write(rc)
    if 'Bledny login lub haslo' in rc:
        acc_info['status'] = 'deleted'
        return acc_info
    elif 'Your IP is banned' in rc:
        raise ModuleError('ip banned')
    elif 'Wyloguj' in rc and 'EXPIRE_DATE_FORMAT2' not in rc:
        acc_info['status'] = 'free'
        return acc_info
    # TRAFFIC_LEFT_ADDITIONAL 16191 MB TRAFFIC_LEFT_ADDITIONAL
    # TRAFFIC_LEFT 20480 MB TRAFFIC_LEFT
    expire_date = re.search('EXPIRE_DATE_FORMAT2 ([0-9\- :]+) EXPIRE_DATE_FORMAT2', rc).group(1)
    acc_info['status'] = 'premium'
    acc_info['expire_date'] = parser.parse(expire_date)
    return acc_info
