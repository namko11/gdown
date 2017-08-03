# -*- coding: utf-8 -*-

"""
gdown.modules.ipvanish
~~~~~~~~~~~~~~~~~~~

This module contains handlers for ipvanish.

"""

import re
from dateutil import parser
# from datetime import datetime, timedelta
# from bs4 import BeautifulSoup

from ..module import browser, acc_info_template
from ..exceptions import ModuleError


def accInfo(username, passwd, proxy=False):
    """Returns account info."""
    acc_info = acc_info_template()
    r = browser(proxy)
    data = {'username': username,
            'password': passwd,
            'webLogin': 'Login'}
    rc = r.post('https://account.ipvanish.com/index.php', data=data).text
    open('gdown.log', 'w').write(rc)
    #     status = re.search('<b>Account Status:</b></span>\n    <span class="profile_label">(.+?)</span>', rc).group(1)
    if 'Access Denied: Failed attempt limit reached.' in rc:
        raise ModuleError('ip banned')
    elif '<span class="profile_label">Active</span>' in rc:
        acc_info['status'] = 'premium'
        expire_date = re.search('Renewal Date:</b></span>\n<span class="profile_label">([0-9/]+?)</span>', rc).group(1)
        acc_info['expire_date'] = parser.parse(expire_date)
    elif 'Sorry, invalid credentials. Please try again.' in rc:
        acc_info['status'] = 'deleted'
    else:
        raise ModuleError('Unknown status.')
    return acc_info
