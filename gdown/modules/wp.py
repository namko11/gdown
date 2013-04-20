# -*- coding: utf-8 -*-

"""
gdown.modules.wp
~~~~~~~~~~~~~~~~~~~

This module contains handlers for wp.

"""

from ..module import browser, acc_info_template
from ..exceptions import ModuleError


def accInfo(username, passwd):
    """Returns account info."""
    acc_info = acc_info_template()
    r = browser()
    r.get('https://profil.wp.pl/login_poczta.html')
    data = {'_action': 'login', 'enticket': '', 'idu': '99', 'serwis': '', 'url': '//poczta.wp.pl/index.html', 'login_username': username, 'login_password': passwd, 'mini': '1', '': ''}
    rc = r.post('https://profil.wp.pl/login_poczta.html', data).content
    if 'Wyloguj' in rc:
        acc_info['status'] = 'free'
        return acc_info
    elif 'Konto zablokowane administracyjnie.' in rc:
        acc_info['status'] = 'blocked'
        return acc_info
    elif 'Niestety podany login lub has' in rc:
        acc_info['status'] = 'deleted'
        return acc_info
    else:
        open('gdown.log', 'w').write(rc)
        raise ModuleError('Unknown error, full log in gdown.log')
