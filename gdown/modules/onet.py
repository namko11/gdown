# -*- coding: utf-8 -*-

"""
gdown.modules.onet
~~~~~~~~~~~~~~~~~~~

This module contains handlers for onet.

"""

from ..module import browser, acc_info_template
from ..exceptions import ModuleError


def accInfo(username, passwd):
    """Returns account info."""
    acc_info = acc_info_template()
    r = browser()
    data = {'noscript': '1', 'login': username, 'password': passwd, 'perm': '1'}
    rc = r.post('https://konto.onet.pl/login.html?app_id=poczta.onet.pl.front', data).content
    if any(i in rc for i in ('Wprowadź poprawny adres e-mail.', 'Nieistniejący login.', 'Niepoprawne hasło.')):
        acc_info['status'] = 'deleted'
    elif 'Wyloguj się' in rc:
        acc_info['status'] = 'free'
    else:
        open('gdown.log', 'w').write(rc)
        raise ModuleError('Unknown error, full log in gdown.log')
    return acc_info
