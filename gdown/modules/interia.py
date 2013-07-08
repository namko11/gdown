# -*- coding: utf-8 -*-

"""
gdown.modules.interia
~~~~~~~~~~~~~~~~~~~

This module contains handlers for interia.

"""

from ..module import browser, acc_info_template
from ..exceptions import ModuleError


def accInfo(username, passwd, proxy=False):
    """Returns account info."""
    acc_info = acc_info_template()
    r = browser(proxy)
    r.get('https://poczta.interia.pl')
    data = {'email': username, 'pass': passwd, 'permanent': '1', 'formHTTP': '1', 'webmailSelect': 'classicMail', 'formSubmit': ''}  # 'webmailSelect': 'htmlMail'
    rc = r.post('https://logowanie.interia.pl/poczta/zaloguj', data).content
    if any(i in rc for i in ('Konto zostało zablokowane', 'Blokada konta', 'Nie możesz już korzystać ze swojej skrzynki pocztowej')):
        acc_info['status'] = 'blocked'
    elif 'Błędny login lub hasło' in rc:
        acc_info['status'] = 'deleted'
    elif 'Wyloguj' in rc:
        acc_info['status'] = 'free'
    else:
        open('gdown.log', 'w').write(rc)
        raise ModuleError('Unknown error, full log in gdown.log')
    return acc_info
