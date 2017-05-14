# -*- coding: utf-8 -*-

"""
gdown.modules.wp
~~~~~~~~~~~~~~~~~~~

This module contains handlers for wp.

"""

from ..module import browser, acc_info_template
from ..exceptions import ModuleError


def accInfo(username, passwd, proxy=False):
    """Returns account info."""
    acc_info = acc_info_template()
    r = browser(proxy)
    r.get('https://profil.wp.pl/login_poczta.html')
    data = {'_action': 'login', 'enticket': '', 'idu': '99', 'serwis': '', 'url': '//poczta.wp.pl/index.html', 'login_username': username, 'login_password': passwd, 'mini': '1', '': ''}
    rc = r.post('https://profil.wp.pl/login_poczta.html', data).text
    if 'Wyloguj' in rc:
        acc_info['status'] = 'free'
    elif 'Konto zablokowane administracyjnie.' in rc:
        acc_info['status'] = 'blocked'
    elif 'Niestety podany login lub has' in rc:
        acc_info['status'] = 'deleted'
    else:
        open('gdown.log', 'w').write(rc)
        raise ModuleError('Unknown error, full log in gdown.log')
    return acc_info
