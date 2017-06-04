# -*- coding: utf-8 -*-

"""
gdown.modules.keep2share
~~~~~~~~~~~~~~~~~~~

This module contains handlers for keep2share.

"""

import re
from datetime import datetime
# from dateutil import parser

from ..module import browser, acc_info_template
from ..exceptions import ModuleError


def accInfo(username, passwd, proxy=False):
    """Returns account info."""
    acc_info = acc_info_template()
    r = browser(proxy)
    rc = r.get('https://keep2share.cc/login.html').text
    if 'LoginForm_verifyCode' in rc:
        print('captcha')
        raise ModuleError('CAPTCHA')
    csrf_token = re.search('value\="(.+?)" name\="YII_CSRF_TOKEN"', rc).group(1)
    data = {'LoginForm[username]': username,
            'LoginForm[password]': passwd,
            'LoginForm[rememberMe]': 0,
            'YII_CSRF_TOKEN': csrf_token}
    rc = r.post('https://keep2share.cc/login.html', data=data).text  #

    if '<a href="/premium.html" class="free" style="color: red">free</a>' in rc:
        acc_info['status'] = 'free'
        return acc_info
    elif 'You account was used from a different countries and automatically locked for security reasons.' in rc:
        acc_info['status'] = 'blocked'
        return acc_info
    elif 'Incorrect username or password' in rc:
        acc_info['status'] = 'deleted'
        return acc_info
    elif 'Premium expires: ' in rc:
        acc_info['status'] = 'premium'
        if '<b>LifeTime</b>' in rc:
            acc_info['expire_date'] = datetime.max
        else:
            d = re.search('Premium expires: <b>([0-9]{4})\.([0-9]{2})\.([0-9]{2})</b>', rc)
            acc_info['expire_date'] = datetime(int(d.group(1)), int(d.group(2)), int(d.group(3)))
        return acc_info
    else:
        open('gdown.log', 'w').write(rc)
        raise ModuleError('Unknown error, full log in gdown.log')
