# -*- coding: utf-8 -*-

"""
gdown.modules.expressvpn
~~~~~~~~~~~~~~~~~~~

This module contains handlers for expressvpn.

"""

import re
from datetime import datetime, timedelta

from ..module import browser, acc_info_template
from ..exceptions import ModuleError


def accInfo(username, passwd, proxy=False):
    """Returns account info."""
    acc_info = acc_info_template()
    r = browser(proxy)
    rc = r.get('https://www.expressvpn.com/users/sign_in').text
    open('gdown.log', 'w').write(rc)
    token = re.search('name="authenticity_token" type="hidden" value="(.+?)"', rc).group(1)
    data = {'utf8': '✓',
            'authenticity_token': token,
            'user[email]': username,
            'user[password]': passwd,
            'commit': 'Sign In'}
    r.headers['Referer'] = 'https://www.expressvpn.com/pl/users/sign_in'
    rc = r.post('https://www.expressvpn.com/users/sign_in', data=data).text
    open('gdown.log', 'w').write(rc)
