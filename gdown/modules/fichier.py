# -*- coding: utf-8 -*-

"""
gdown.modules.1fichier
~~~~~~~~~~~~~~~~~~~

This module contains handlers for 1fichier.

"""

import re
from dateutil import parser

from ..module import browser, acc_info_template
from ..exceptions import ModuleError


def accInfo(username, passwd, proxy=False):
    acc_info = acc_info_template()
    r = browser()
    data = {'mail': username, 'pass': passwd, 'valider': 'Send'}
    rc = r.post('https://1fichier.com/login.pl', data).text
    open('gdown.log', 'w').write(rc)
    if 'Invalid username.' in rc or 'Invalid email address.' in rc or 'Invalid username or Password.' in rc or 'Invalid password.' in rc:
        if 'Warning ! You have only 0 try left' in rc:
            print('NO MORE TRIES')
            asddsasaddsa
        acc_info['status'] = 'deleted'
        return acc_info
    elif 'For security reasons, following many identification errors, your IP address (' in rc:
        raise ModuleError('ip AND ACC blocked')
    elif 'Logout' not in rc:
        print('?')
        asdasddas
    rc = r.get('https://1fichier.com/console/abo.pl').text
    open('gdown.log', 'w').write(rc)
    if 'Your Premium offer subscription is valid until' in rc:  # premium
        expire_date = re.search('Your Premium offer subscription is valid until <span style="font-weight:bold">([0-9]{4}\-[0-9]{2}\-[0-9]{2})</span>', rc).group(1)
        acc_info['status'] = 'premium'
        acc_info['expire_date'] = parser.parse(expire_date)
        return acc_info
    elif 'Your Access offer subscription is valid until' in rc:  # access (~half-premium)
        expire_date = re.search('Your Access offer subscription is valid until <span style="font-weight:bold">([0-9]{4}\-[0-9]{2}\-[0-9]{2})</span>', rc).group(1)
        acc_info['status'] = 'premium'
        acc_info['expire_date'] = parser.parse(expire_date)
        return acc_info
    elif 'Your Premium offer subscription is valid' not in rc:
        acc_info['status'] = 'free'
        return acc_info
    else:
        raise ModuleError('unknown status')
