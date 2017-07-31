# -*- coding: utf-8 -*-

"""
gdown.modules.nordvpn
~~~~~~~~~~~~~~~~~~~

This module contains handlers for nordvpn.

"""

# import re
# from dateutil import parser
# from datetime import datetime, timedelta
# from bs4 import BeautifulSoup

from ..module import browser, acc_info_template
from ..exceptions import ModuleError


def accInfo(username, passwd, proxy=False):
    """Returns account info."""
    acc_info = acc_info_template()
    r = browser(proxy)
    data = {'log': username,
            'pwd': passwd,
            'wp-submit': 'Log In',
            'testcookie': 1,
            'redirect_to': 'https://nordvpn.com/profile/',
            '_mgmnonce_user_login': '56c72d0fc6',  # ?
            '_wp_http_referer': '/login/'}
    rc = r.post('https://nordvpn.com/login/', data=data).text
    if 'Your account has expired.' in rc:
        acc_info['status'] = 'free'
    else:
        open('gdown.log', 'w').write(rc)
        raise ModuleError('Unknown response.')
    return acc_info
