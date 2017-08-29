# -*- coding: utf-8 -*-

"""
gdown.modules.depfile
~~~~~~~~~~~~~~~~~~~

This module contains handlers for depfile.

"""

import re
import time
from dateutil import parser

from ..module import browser, acc_info_template
from ..exceptions import ModuleError


def accInfo(username, passwd, proxy=False):
    acc_info = acc_info_template()
    r = browser()
    data = {'login': 'login', 'loginemail': username, 'loginpassword': passwd, 'submit': 'login', 'rememberme': 'on', 'language': 2}
    rc = r.post('https://depfile.com', data=data).text
    open('gdown.log', 'w').write(rc)
    if 'Incorrect password' in rc or 'E-mail not found.' in rc or 'Please enter your E-mail.' in rc:  # same error if ip banned
        acc_info['status'] = 'deleted'
        return acc_info
    elif 'Enter TOTP:' in rc:
        # raise ModuleError('TOTP required')
        acc_info['status'] = 'deleted'
        return acc_info
    elif 'You are banned' in rc:
        acc_info['status'] = 'blocked'
        return acc_info
    elif '502 Bad Gateway' in rc:
        print('502 Bad Gateway')
        time.sleep(1)
        return accInfo(username=username, passwd=passwd, proxy=proxy)
    elif 'uploads/logout' not in rc:
        raise ModuleError('unknown status')
    data = {'SetLng': 'SetLng',
            'language': '2'}
    rc = r.post('https://depfile.com/myspace/space/personal', data=data).text
    open('gdown2.log', 'w').write(rc)
    expire_date = re.search("href='/myspace/space/premium'>(.+?)<img", rc)
    if 'Premium account expired' in rc:
        acc_info['status'] = 'free'
    elif expire_date:
        expire_date = expire_date.group(1)
        acc_info['status'] = 'premium'
        acc_info['expire_date'] = parser.parse(expire_date)
    elif '502 Bad Gateway2' in rc:
        print('502 Bad Gateway')
        time.sleep(1)
        return accInfo(username=username, passwd=passwd, proxy=proxy)
    elif 'uploads/logout' in rc:
        acc_info['status'] = 'free'
    else:
        raise ModuleError('Unknown status')
    return acc_info
