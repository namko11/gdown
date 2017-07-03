# -*- coding: utf-8 -*-

"""
gdown.modules.filejoker
~~~~~~~~~~~~~~~~~~~

This module contains handlers for filejoker.

"""

import re
from datetime import datetime

from ..module import browser, acc_info_template


def accInfo(username, passwd, proxy=False):
    """Returns account info."""
    acc_info = acc_info_template()
    r = browser(proxy)
    data = {'email': username,
            'password': passwd,
            'op': 'login',
            'redirect': '',
            'rand': ''}
    rc = r.post('https://filejoker.net/login', data=data).text
    open('gdown.log', )
    acc_info['transfer'] = re.search('<td>Traffic Available:</td>\n<td>([0-9 MGB]+?)</td>', rc).group(1)  # not tested
    if 'Premium account expires:' in rc:
        acc_info['status'] = 'premium'
        print(re.search('Premium account expires: ([0-9 a-Z]+?)\n', rc).group(1))
        asdasdsa
        # acc_info['expire_date'] =
    else:
        asddsadsadsa
