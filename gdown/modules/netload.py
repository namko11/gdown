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
    r = browser()
    values = {'txtuser': username, 'txtpass': passwd, 'txtcheck': 'login', 'txtlogin': 'Login'}
    r.post('https://netload.in/index.php', values)
    return r.get(link).url  # return connection


def accInfo(username, passwd, proxy=False):
    """Returns account info."""
    acc_info = acc_info_template()
    r = browser(proxy)
    values = {'txtuser': username, 'txtpass': passwd, 'txtcheck': 'login', 'txtlogin': 'Login'}
    r.post('https://netload.in/index.php', values)
    content = r.get('https://netload.in/index.php?id=15').text
    if 'This account was locked' in content or'Sorry, please activate first your account.' in content:  # account not activated
        acc_info['status'] = 'blocked'
        return acc_info
    elif 'not found in our records!' in content or 'Invalid User ID or password!' in content:
        acc_info['status'] = 'deleted'
        return acc_info
    elif 'Please wait a moment before tryingto log in again!' in content:   # ip blocked
        raise IpBlocked
    rc = r.get('https://netload.in/index.php?id=2').text
    content = re.search('<div class="num">([0-9d, h\-]+?)</div>\n[ ]{16}<h3>Remaining Premium</h3>', rc).group(1)
    if content == '-':
        acc_info['status'] = 'free'
    else:
        acc_info['status'] = 'premium'
        acc_info['expire_date'] = datetime.utcnow()
        content = content.split(', ')
        for i in content:
            if i.endswith('d'):  # days
                acc_info['expire_date'] = acc_info['expire_date'] + timedelta(days=int(i[:-1]))
            elif i.endswith('h'):  # hours
                acc_info['expire_date'] = acc_info['expire_date'] + timedelta(hours=int(i[:-1]))
    return acc_info


def upload(username, passwd, filename):
    """Returns uploaded file url."""
    r = browser()
    host = r.get('http://api.netload.in/getserver.php').text
    content = r.post(host, {'user_id': username, 'user_password': passwd, 'modus': 'file_upload'}, files={'file': open(filename, 'rb')}).text
    return re.search('UPLOAD_OK;.+;[0-9]+;(.+);.+', content).group(1)
