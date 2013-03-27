# -*- coding: utf-8 -*-

import requests
import time
import re

from ..config import headers
from ..exceptions import IpBlocked, AccountBlocked, AccountRemoved


def getUrl(link, username, passwd):
    """Returns direct file url.
    IP validator is present."""
    opera = requests.session(headers=headers)
    values = {'txtuser': username, 'txtpass': passwd, 'txtcheck': 'login', 'txtlogin': ''}
    opera.post('http://netload.in/index.php', values)
    return opera.get(link).url  # return connection


def status(username, passwd):
    """Returns account premium status."""
    opera = requests.session(headers=headers)
    values = {'txtuser': username, 'txtpass': passwd, 'txtcheck': 'login', 'txtlogin': 'Login'}
    opera.post('http://netload.in/index.php', values)
    content = opera.get('http://netload.in/index.php?id=15').content
    if 'This account was locked' in content or'Sorry, please activate first your account.' in content:  # account not activated
        raise AccountBlocked
    elif 'not found in our records!' in content or 'Invalid User ID or password!' in content:
        raise AccountRemoved
    elif 'Please wait a moment before tryingto log in again!' in content:   # ip blocked
        raise IpBlocked
    content = opera.get('http://netload.in/index.php?id=2').content
    if 'No Bonus' in content or 'Kein Premium' in content:
        return 0
    else:
        content = re.search('<div style="float: left; width: 150px; color: #FFFFFF;"><span style="color: green">([0-9]*?)[ Tage,]{,7}([0-9]+) Stunden</span></div>', content)
        if content.group(1):
            return time.time() + int(content.group(1)) * 24 * 60 * 60 + int(content.group(2)) * 60 * 60
        else:
            return time.time() + int(content.group(2)) * 60 * 60


def upload(username, passwd, filename):
    """Returns uploaded file url."""
    opera = requests.session(headers=headers)
    host = opera.get('http://api.netload.in/getserver.php').content
    content = opera.post(host, {'user_id': username, 'user_password': passwd, 'modus': 'file_upload'}, files={'file': open(filename, 'rb')}).content
    return re.search('UPLOAD_OK;.+;[0-9]+;(.+);.+', content).group(1)
