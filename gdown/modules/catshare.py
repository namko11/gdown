# -*- coding: utf-8 -*-

"""
gdown.modules.uploaded
~~~~~~~~~~~~~~~~~~~

This module contains handlers for uploaded.

"""

import re
from datetime import datetime, timedelta
from time import sleep
from decimal import Decimal

from ..module import browser, acc_info_template


def accInfo(username, passwd, proxy=False):
    """Returns account info."""
    acc_info = acc_info_template()
    r = browser(proxy)
    data = {'user_email': username, 'user_password': passwd}
    rc = r.post('https://catshare.net/login', data).text
    if 'Podane hasło jest nieprawidłowe' in rc:
        acc_info['status'] = 'deleted'
    elif '<span style="color: red">Darmowe</span>' in rc:
        acc_info['status'] = 'free'
    elif '<span class="hidden-xs">Premium</span>' in rc:
        expire_date = datetime.utcnow()
        acc_info['status'] = 'premium'
        open('gdown.log', 'w').write(rc)  # DEBUG
        if 'godzin</span></b>' in rc:  # < 1 day
            acc_info['expire_date'] = expire_date + timedelta(days=1)
        else:
            s = re.search('<span class="hidden-xs">Premium</span> <b>([0-9]+) dni</b> \( ([0-9\.]+ GB) \)', rc)
            '''
            if seconds:
                expire_date += timedelta(seconds=int(seconds.group(1)))
            if minutes:
                expire_date += timedelta(minutes=int(minutes.group(1)))
            if hours:
                expire_date += timedelta(hours=int(hours.group(1)))
            if days:
                expire_date += timedelta(days=int(days.group(1)))
            if weeks:
                expire_date += timedelta(weeks=int(weeks.group(1)))
            '''
            expire_date += timedelta(days=int(s.group(1)))
            acc_info['expire_date'] = expire_date
            acc_info['transfer'] = s.group(2)
    else:
        open('gdown.log', 'w').write(rc)  # DEBUG
        asdasdadasd
    return acc_info
