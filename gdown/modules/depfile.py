# -*- coding: utf-8 -*-

"""
gdown.modules.depfile
~~~~~~~~~~~~~~~~~~~

This module contains handlers for depfile.

"""

import re
from dateutil import parser

from ..module import browser, acc_info_template


def accInfo(username, passwd, proxy=False):
    acc_info = acc_info_template()
    r = browser()
    data = {'login': 'login', 'loginemail': username, 'loginpassword': passwd, 'submit': 'login', 'rememberme': 'on'}
    rc = r.post('https://depfile.com', data).text
    open('gdown.log', 'w').write(rc)
    if 'Premium account expired' in rc:
        acc_info['status'] = 'free'
        return acc_info
    expire_date = re.search("href='/myspace/space/premium'>(.+?)<img", rc).group(1)
    acc_info['status'] = 'premium'
    acc_info['expire_date'] = parser.parse(expire_date)
    return acc_info
