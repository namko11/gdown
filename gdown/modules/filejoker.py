# -*- coding: utf-8 -*-

"""
gdown.modules.filejoker
~~~~~~~~~~~~~~~~~~~

This module contains handlers for filejoker.

"""

import re
# import time
from dateutil import parser
# from datetime import datetime

from ..module import browser, acc_info_template
from ..exceptions import ModuleError


def accInfo(username, passwd, proxy=False):
    """Returns account info."""
    acc_info = acc_info_template()
    r = browser(proxy)
    data = {'email': username,
            'password': passwd,
            'op': 'login',
            'redirect': '',
            'rand': ''}
    rc = r.post('https://filejoker.net/login', data=data).text
    open('gdown.log', 'w').write(rc)

    if 'Why do I have to complete a CAPTCHA?' in rc:
        # print('captcha')
        # time.sleep(5)
        # return accInfo(username=username, passwd=passwd, proxy=proxy)
        raise ModuleError('captcha')
    elif 'Incorrect Login or Password' in rc or 'Invalid email' in rc:
        acc_info['status'] = 'deleted'
    elif 'Premium account expires:' in rc:
        acc_info['status'] = 'premium'
        acc_info['transfer'] = re.search('<td>Traffic Available:</td>\n<td>([0-9 MGB]+?)</td>', rc).group(1)
        expire_date = re.search('Premium account expires: ([0-9 a-zA-Z]+?)\n', rc).group(1)
        acc_info['expire_date'] = parser.parse(expire_date)
    elif 'Buy Premium' in rc:  # kinda blind guess
        acc_info['status'] = 'free'
    else:
        raise ModuleError('unknown error')
    return acc_info
