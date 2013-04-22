# -*- coding: utf-8 -*-

"""
gdown.modules.interia
~~~~~~~~~~~~~~~~~~~

This module contains handlers for interia.

"""

from ..module import browser, acc_info_template
from ..exceptions import ModuleError


def accInfo(username, passwd):
    """Returns account info."""
    acc_info = acc_info_template()
    r = browser()
    r.get('https://poczta.interia.pl')
    data = {'email': username, 'pass': passwd, 'permanent': '1', 'formHTTP': '1', 'webmailSelect': 'classicMail', 'formSubmit': ''}  # 'webmailSelect': 'htmlMail'
    rc = r.post('https://logowanie.interia.pl/poczta/zaloguj', data).content
    if any(i in rc for i in ('Konto zostało zablokowane', 'Blokada konta', 'Nie możesz już korzystać ze swojej skrzynki pocztowej')):
        acc_info['status'] = 'blocked'
        return acc_info
    elif 'Błędny login lub hasło' in rc:
        acc_info['status'] = 'deleted'
        return acc_info
    elif 'Wyloguj' in rc:
        acc_info['status'] = 'free'
        return acc_info
    else:
        open('gdown.log', 'w').write(rc)
        raise ModuleError('Unknown error, full log in gdown.log')
