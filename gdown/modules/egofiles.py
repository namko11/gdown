# -*- coding: utf-8 -*-

"""
gdown.modules.egofiles
~~~~~~~~~~~~~~~~~~~

This module contains handlers for egofiles.

"""

import re
from simplejson import JSONDecoder
from dateutil import parser

from ..module import browser, acc_info_template
from ..exceptions import ModuleError


def accInfo(username, passwd):
    """Returns account info."""
    acc_info = acc_info_template()
    r = browser()
    data = {'log': '1', 'loginV': username, 'passV': passwd}
    rc = JSONDecoder().decode(r.post('http://egofiles.com/ajax/register.php', data).content)
    if rc.get('error') in (u'Login może mieć 4-16 znaków: a-z, A-Z i 0-9', u'Wpisane hasło jest błędne'):
        acc_info['status'] = 'deleted'
    elif rc.get('ok') == 'Zalogowano.':
        rc = r.get('http://egofiles.com/settings').content
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
