# -*- coding: utf-8 -*-

"""
gdown.modules.hotfile
~~~~~~~~~~~~~~~~~~~

This module contains handlers for hotfile.

"""

import re
import os
from dateutil import parser

from ..module import browser, acc_info_template
from ..exceptions import ModuleError, IpBlocked


def getUrl(link, username, passwd):
    """Returns direct file url.
    IP validator is present."""
    r = browser()
    link = r.get('http://api.hotfile.com/?action=getdirectdownloadlink&username=%s&password=%s&link=%s' % (username, passwd, link)).content
    return r.get(link).url  # return connection


def accInfo(username, passwd):
    """Returns account info."""
    acc_info = acc_info_template()
    r = browser()
    content = r.get('http://api.hotfile.com/?action=getuserinfo&username=%s&password=%s' % (username, passwd)).content
    if 'is_premium=1' in content:   # premium
        acc_info['status'] = 'premium'
        expire_date = re.search('premium_until=(.+?)&', content).group(1)
        acc_info['expire_date'] = parser.parse(expire_date, ignoretz=True)
        return acc_info
    elif 'is_premium=0' in content:  # free
        acc_info['status'] = 'free'
        return acc_info
    elif 'user account is suspended' in content:  # account suspended (permanent?)
        acc_info['status'] = 'blocked'
        return acc_info
    elif 'invalid username or password' in content:  # invalid username/passwd
        acc_info['status'] = 'deleted'
        return acc_info
    elif 'too many failed attemtps' in content:  # ip blocked
        raise IpBlocked
    else:
        open('gdown.log', 'w').write(content)
        raise ModuleError('Unknown error, full log in gdown.log')


def upload(username, passwd, filename):
    """Returns uploaded file url."""
    file_size = os.path.getsize(filename)   # get file size
    r = browser()
    host = r.get('http://api.hotfile.com/?action=getuploadserver').content[:-1]  # get server to upload
    upload_id = r.post('http://%s/segmentupload.php?action=start' % (host), {'size': file_size}).content[:-1]  # start upload
    r.post('http://%s/segmentupload.php?action=upload' % (host), {'id': upload_id, 'offset': 0}, files={'segment': open(filename, 'rb')}).content  # upload
    return r.post('http://%s/segmentupload.php?action=finish' % (host), {'id': upload_id, 'name': filename, 'username': username, 'password': passwd}).content[:-1]  # start upload
