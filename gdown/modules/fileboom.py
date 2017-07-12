# -*- coding: utf-8 -*-

"""
gdown.modules.uploaded
~~~~~~~~~~~~~~~~~~~

This module contains handlers for uploaded.

"""

import re
from dateutil import parser
# from datetime import datetime, timedelta
# from time import sleep
# from decimal import Decimal

from ..core import captcha
from ..module import browser, acc_info_template


def accInfo(username, passwd, proxy=False):
    """Returns account info."""
    acc_info = acc_info_template()
    r = browser(proxy)
    rc = r.get('https://fileboom.me/login.html').text
    open('gdown.log', 'w').write(rc)
    csrf_token = re.search('value="(.+?)" name="YII_CSRF_TOKEN"', rc).group(1)
    data = {'YII_CSRF_TOKEN': csrf_token,
            'LoginForm[username]': username,
            'LoginForm[password]': passwd,
            'LoginForm[rememberMe]': 0}
    if 'LoginForm[verifyCode]' in rc:
        print('CAPTCHA')
        img_url = 'https://fileboom.me' + re.search('id="captcha_auth1" src="(/auth/captcha.html\?v=.+?)"', rc).group(1)
        img = r.get(img_url).content
        data['LoginForm[verifyCode]'] = captcha(img)  # TODO: verification (False)
    rc = r.post('https://fileboom.me/login.html', data=data).text
    open('gdown.log', 'w').write(rc)
    if 'Incorrect username or password' in rc:
        acc_info['status'] = 'deleted'
    rc = r.get('https://fileboom.me/site/profile.html').text  # TODO?: redirect on login?
    expire_date = re.search('Premium expires:            <b>([0-9\.]+)</b>', rc)
    if expire_date:
        acc_info['status'] = 'premium'
        acc_info['expire_date'] = parser.parse(expire_date.group(1))
    return acc_info
