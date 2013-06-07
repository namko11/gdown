# -*- coding: utf-8 -*-

"""
gdown.modules.ryushare
~~~~~~~~~~~~~~~~~~~

This module contains handlers for ryushare.

"""

import re
from dateutil import parser

from ..module import browser, acc_info_template
from ..exceptions import ModuleError, IpBlocked


def accInfo(username, passwd):
    """Returns account info."""
    acc_info = acc_info_template()
    r = browser()
    content = r.post('http://ryushare.com', {'op': 'login', 'redirect': 'http://ryushare.com/my-account.python', 'login': username, 'password': passwd, 'loginFormSubmit': 'Login'}).content
    if any(i in content for i in ('Your account was banned by administrator.', "Your account haven't confirmed yet.")):
        acc_info['status'] = 'blocked'
        return acc_info
    elif 'Incorrect Login or Password' in content:
        acc_info['status'] = 'deleted'
        return acc_info
    elif any(i in content for i in ('Your IP was blocked because too many logins fail.', 'Your IP was had too many fail login!!!')):
        raise IpBlocked
    elif 'Premium account expire:' in content:
        acc_info['status'] = 'premium'
        acc_info['expire_date'] = parser.parse(re.search('Premium account expire:</TD><TD><b>(.+)</b>', content).group(1))
        return acc_info
    elif '<a class="logout" href="http://ryushare.com/logout">&nbsp;Logout</a>' in content:
        acc_info['status'] = 'free'
        return acc_info
    else:
        open('gdown.log', 'w').write(content)
        raise ModuleError('Unknown error, full log in gdown.log')
