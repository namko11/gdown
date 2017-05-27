# -*- coding: utf-8 -*-

"""
gdown.modules.1fichier
~~~~~~~~~~~~~~~~~~~

This module contains handlers for 1fichier.

"""

import re
from dateutil import parser

from ..module import browser, acc_info_template


def accInfo(username, passwd, proxy=False):
    acc_info = acc_info_template()
    r = browser()
    data = {'mail': username, 'pass': passwd, 'valider': 'Send'}
    rc = r.post('https://1fichier.com/login.pl', data).text
    open('log.log', 'w').write(rc)
    if 'Invalid username.' in rc:
        acc_info['status'] = 'deleted'
        return acc_info
    elif 'For security reasons, following many identification errors, your IP address (176.9.140.205) is temporarily locked.':
        print('ip AND ACC blocked')
        asdasdsad
    elif 'Logout' not in rc:
        print('?')
        asdasddas
    rc = r.get('https://1fichier.com/console/abo.pl').text
    expire_date = re.search('Your Premium offer subscription is valid until <span style="font-weight:bold">([0-9]{4}\-[0-9]{2}\-[0-9]{2})</span>', rc).group(1)
    acc_info['status'] = 'premium'
    acc_info['expire_date'] = parser.parse(expire_date)
    return acc_info
