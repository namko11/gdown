# -*- coding: utf-8 -*-

"""
gdown.modules.netload
~~~~~~~~~~~~~~~~~~~

This module contains handlers for netload.

"""

import re
from datetime import datetime, timedelta

from ..module import browser, acc_info_template
from ..exceptions import IpBlocked


def getUrl(link, username, passwd):
    """Returns direct file url.
    IP validator is present."""
    opera = browser()
    values = {'txtuser': username, 'txtpass': passwd, 'txtcheck': 'login', 'txtlogin': ''}
    opera.post('http://netload.in/index.php', values)
    return opera.get(link).url  # return connection


def accInfo(username, passwd):
    """Returns account info."""
    acc_info = acc_info_template()
    opera = browser()
    values = {'txtuser': username, 'txtpass': passwd, 'txtcheck': 'login', 'txtlogin': 'Login'}
    opera.post('http://netload.in/index.php', values)
    content = opera.get('http://netload.in/index.php?id=15').content
    if 'This account was locked' in content or'Sorry, please activate first your account.' in content:  # account not activated
        acc_info['status'] = 'blocked'
        return acc_info
    elif 'not found in our records!' in content or 'Invalid User ID or password!' in content:
        acc_info['status'] = 'deleted'
        return acc_info
    elif 'Please wait a moment before tryingto log in again!' in content:   # ip blocked
        raise IpBlocked
    content = opera.get('http://netload.in/index.php?id=2').content
    if 'No Bonus' in content or 'Kein Premium' in content:
        acc_info['status'] = 'free'
        return acc_info
    else:
        content = re.search('<div style="float: left; width: 150px; color: #FFFFFF;"><span style="color: green">([0-9]*?)[ Tage,]{,7}([0-9]+) Stunden</span></div>', content)
        acc_info['status'] = 'premium'
        if content.group(1):
            acc_info['expire_date'] = datetime.utcnow() + timedelta(days=int(content.group(1)), hours=int(content.group(2)))
        else:
            acc_info['expire_date'] = datetime.utcnow() + timedelta(hours=int(content.group(2)))
        return acc_info


def upload(username, passwd, filename):
    """Returns uploaded file url."""
    opera = browser()
    host = opera.get('http://api.netload.in/getserver.php').content
    content = opera.post(host, {'user_id': username, 'user_password': passwd, 'modus': 'file_upload'}, files={'file': open(filename, 'rb')}).content
    return re.search('UPLOAD_OK;.+;[0-9]+;(.+);.+', content).group(1)
