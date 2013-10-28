# -*- coding: utf-8 -*-

"""
gdown.modules.egofiles
~~~~~~~~~~~~~~~~~~~

This module contains handlers for egofiles.

"""

from __future__ import unicode_literals

import re
from dateutil import parser

from ..module import browser, acc_info_template
from ..exceptions import ModuleError, IpBlocked


def accInfo(username, passwd, proxy=False):
    """Returns account info."""
    acc_info = acc_info_template()
    r = browser(proxy)
    data = {'log': '1', 'loginV': username, 'passV': passwd}
    rc = r.post('http://egofiles.com/ajax/register.php', data).json()
    if rc.get('error') in ('Login może mieć 4-16 znaków: a-z, A-Z i 0-9', 'Wpisane hasło jest błędne', 'Podany login nie istnieje'):
        acc_info['status'] = 'deleted'
    elif rc.get('error') == 'Przekroczono limit prób - odczekaj chwilę i spróbuj ponownie':
        raise IpBlocked
    elif rc.get('ok') == 'Zalogowano.':
        rc = r.get('http://egofiles.com/settings').text
        if 'Korzystasz z konta Free User' in rc:
            acc_info['status'] = 'free'
        elif 'Korzystasz z konta Premium' in rc:
            acc_info['status'] = 'premium'
            acc_info['expire_date'] = parser.parse(re.search('Premium: ([0-9\-]{10} [0-9:]{8}) /', rc).group(1))
        else:
            open('gdown.log', 'w').write(rc)
            raise ModuleError('Unknown account status, full log in gdown.log')
    else:
        open('gdown.log', 'w').write(rc)
        raise ModuleError('Unknown error, full log in gdown.log')
    return acc_info
