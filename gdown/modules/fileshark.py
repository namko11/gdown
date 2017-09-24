# -*- coding: utf-8 -*-

"""
gdown.modules.fileshark
~~~~~~~~~~~~~~~~~~~

This module contains handlers for fileshark.

"""

import re
# from datetime import datetime
from dateutil import parser
from requests.exceptions import ConnectionError

from ..module import browser, acc_info_template
from ..exceptions import ModuleError


def accInfo(username, passwd, proxy=False):
    """Returns account info."""
    r = browser(proxy)
    acc_info = acc_info_template()
    # r.headers['X-Requested-With'] = 'XMLHttpRequest'
    try:
        rc = r.get('http://fileshark.pl/zaloguj')
    except ConnectionError as e:
        raise ModuleError('ip banned')
    open('gdown.log', 'w').write(rc.text)
    csrf_token = re.search('name="_csrf_token" value="(.+?)"', rc.text).group(1)
    data = {'_username': username,
            '_password': passwd,
            '_csrf_token': csrf_token}
    rc = r.post('http://fileshark.pl/login_check', data=data).text
    open('gdown.log', 'w').write(rc)

    if 'Rodzaj konta <strong>Premium' in rc:
        acc_info['status'] = 'premium'
        date_expire = re.search('Premium <span title="([0-9\- \:]+?)"', rc).group(1)
        acc_info['expire_date'] = parser.parse(date_expire)
        rc = re.search('data-min="0" data-max="([0-9]+)" data-angleOffset=90 data-linecap=round value="([0-9]+)"', rc)
        acc_info['transfer'] = int((int(rc.group(1)) - int(rc.group(2))) / 1024 / 1024 / 1024)
    elif 'Rodzaj konta <strong>Standardowe' in rc:
        acc_info['status'] = 'free'
    elif 'Nieprawidłowe dane.' in rc:
        acc_info['status'] = 'deleted'
    else:
        pasddassad
    return acc_info
