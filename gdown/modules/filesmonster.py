# -*- coding: utf-8 -*-

"""
gdown.modules.filesmonter
~~~~~~~~~~~~~~~~~~~

This module contains handlers for filesmonster.

"""

import re
from datetime import datetime

from ..module import browser, acc_info_template
from ..exceptions import ModuleError, IpBlocked


def accInfo(username, passwd, proxy=False):
    """Returns account info."""
    acc_info = acc_info_template()
    r = browser(proxy)
    data = {'act': 'login', 'user': username, 'pass': passwd, 'captcha_shown': 0, 'login': 'Login'}
    rc = r.post('https://filesmonster.com/login.php', data).text
    open('gdown.log', 'w').write(rc)  # DEBUG
    if 'For security reasons, please enter captcha code below' in rc or 'Please confirm that you are not a robot' in rc:
        print('recaptcha')
        adassa
    elif 'Username/Password can not be found in our database!' in rc:
        acc_info['status'] = 'deleted'
        return acc_info
    elif 'Your account is suspended!' in rc or 'Your account is banned!' in rc:
        acc_info['status'] = 'blocked'
        return acc_info
    elif "<span class='red em'>Expired:" in rc:
        # TODO: parse date
        # <span class='red em'>Expired: 06/25/12</span>
        acc_info['status'] = 'free'
        return acc_info
    # Your membership type: <span class="em lightblack">Premium</span>
