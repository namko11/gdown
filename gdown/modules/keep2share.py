# -*- coding: utf-8 -*-

"""
gdown.modules.keep2share
~~~~~~~~~~~~~~~~~~~

This module contains handlers for keep2share.

"""

import re
from datetime import datetime
from dateutil import parser

from ..module import browser, acc_info_template
from ..exceptions import ModuleError



def accInfo(username, passwd, proxy=False):
    """Returns account info."""
    acc_info = acc_info_template()
    r = browser(proxy)
    rc = r.get('https://keep2share.cc/login.html').text
    csrf_token = re.search('value\="(.+?)" name\="YII_CSRF_TOKEN"', rc).group(1)
    login_form = {'username': username,
                  'password': passwd,
                  'rememberMe': 0}
    rc = r.post('https://keep2share.cc/login.html', {'LoginForm[username]': username, 'LoginForm[password]': passwd, 'LoginForm[rememberMe]': 0, 'YII_CSRF_TOKEN': csrf_token}).text  #

    if '<a href="/premium.html" class="free" style="color: red">free</a>' in rc:
        acc_info['status'] = 'free'
        return acc_info
    else:
        open('gdown.log', 'w').write(rc)
        raise ModuleError('Unknown error, full log in gdown.log')
