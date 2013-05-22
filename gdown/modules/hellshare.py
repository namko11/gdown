# -*- coding: utf-8 -*-

"""
gdown.modules.hellshare
~~~~~~~~~~~~~~~~~~~

This module contains handlers for hellshare.

"""

import re
from dateutil import parser

from ..module import browser, acc_info_template
from ..exceptions import ModuleError


def accInfo(username, passwd):
    """Returns account info."""
    acc_info = acc_info_template()
    r = browser()
    r.get('http://www.hellshare.com')
    r.get('http://www.hellshare.com/?do=login-showLoginWindow')
    #   http://www.hellshare.com/members-auth/login
    values = {'login': 'Log in as registered user', 'username': username, 'password': passwd, 'perm_login': 'on'}
    content = r.post('http://www.hellshare.com/?do=login-loginBoxForm-submit', values).content
    if 'Wrong user name or wrong password' in content:
        acc_info['status'] = 'deleted'
        return acc_info
    content = r.get('http://www.hellshare.com/members/').content
    if 'Active until: ' in content:
        expire_date = re.search('Active until: ([0-9]+\.[0-9]+\.[0-9]+)<br />', content).group(1)
        acc_info['status'] = 'premium'
        acc_info['expire_date'] = parser.parse(expire_date)
        return acc_info
    if 'Inactive' in content:
        acc_info['status'] = 'free'
        return acc_info
    else:
        open('gdown.log', 'w').write(content)
        raise ModuleError('Unknown error, full log in gdown.log')
