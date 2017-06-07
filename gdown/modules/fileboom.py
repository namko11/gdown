# -*- coding: utf-8 -*-

"""
gdown.modules.uploaded
~~~~~~~~~~~~~~~~~~~

This module contains handlers for uploaded.

"""

import re
# from datetime import datetime, timedelta
# from time import sleep
# from decimal import Decimal

from ..module import browser, acc_info_template


def accInfo(username, passwd, proxy=False):
    """Returns account info."""
    acc_info = acc_info_template()
    r = browser(proxy)
    rc = r.get('https://fileboom.me/login.html').text
    if 'LoginForm[verifyCode]' in rc:
        print('captcha')
        asdadsdsa
    csrf_token = re.search('value="(.+?)" name="YII_CSRF_TOKEN"', rc).group(1)
    data = {'YII_CSRF_TOKEN': csrf_token,
            'LoginForm[username]': username,
            'LoginForm[password]': passwd,
            'LoginForm[rememberMe]': 0}
    rc = r.post('https://fileboom.me/login.html', data=data).text
    open('gdown.log', 'w').write(rc)
    if 'Incorrect username or password' in rc:
        acc_info['status'] = 'deleted'
    return acc_info