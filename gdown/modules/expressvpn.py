# -*- coding: utf-8 -*-

"""
gdown.modules.expressvpn
~~~~~~~~~~~~~~~~~~~

This module contains handlers for expressvpn.

"""

import re
from dateutil import parser
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

from ..module import browser, acc_info_template
from ..exceptions import ModuleError


def accInfo(username, passwd, proxy=False):
    """Returns account info."""
    acc_info = acc_info_template()
    r = browser(proxy)
    rc = r.get('https://www.expressvpn.com/users/sign_in').text
    open('gdown.log', 'w').write(rc)
    token = re.search('name="authenticity_token" value="(.+?)"', rc).group(1)
    data = {'utf8': '✓',
            'authenticity_token': token,
            'email': username,
            'password': passwd,
            'commit': 'Sign In'}
    rc = r.post('https://www.expressvpn.com/v2/sessions', data=data).text
    open('gdown.log', 'w').write(rc)
    if 'Invalid email or password.' in rc:
        acc_info['status'] = 'deleted'
    elif 'Expires on' in rc:
        bs = BeautifulSoup(rc, 'lxml')
        expire_date = bs.find('div', class_='table-col c15').contents[2]
        acc_info['status'] = 'premium'
        acc_info['expire_date'] = parser.parse(expire_date)
    elif 'Your account is suspended' in rc and 'As we were unable to verify your billing information, your payment has been refunded.' in rc:
        acc_info['status'] = 'blocked'
    elif 'This subscription expired' in rc:
        acc_info['status'] = 'free'
    elif 'Sign Out' in rc and 'Need 5 or more ExpressVPN licenses?' in rc:  # blind guess
        acc_info['status'] = 'free'
    # TODO: not responding when ip banned (short time) - use timeout
    else:
        print('unknown status')
        asdasdasdasd
    return acc_info
